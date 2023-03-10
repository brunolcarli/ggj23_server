import json
from base64 import b64decode
from random import choice
from collections import defaultdict
import channels_graphql_ws
from ast import literal_eval
from site import ENABLE_USER_SITE
import graphene
from graphql import GraphQLObjectType
from django.conf import settings
from django.contrib.auth.models import User
from server_app.models import Character, ItemOffer, SpawnedEnemy
from server_app.skills import skill_list
from server_app.map_areas import areas, area_transfer_coord_map
from server_app.character_classes import classes, ChracterClass
from server_app.engine import target_position_is_valid, use_skill, RespawnSpots
from server_app.enemies import enemy_list
from server_app.items import item_list, max_currency
from server_app.events import OnCharacterEvent
from server_app.utils import CharacterPublishPayload
from server_app.types import DynamicScalar
from ggj23.settings import GAME_CONFIG


chats = defaultdict(list)


class Message(  # type: ignore
    graphene.ObjectType, default_resolver=graphene.types.resolver.dict_resolver
):
    """Message GraphQL type."""

    id = graphene.ID()
    chatroom = graphene.String()
    text = graphene.String()
    sender = graphene.String()


class MapAreaType(graphene.ObjectType):
    name = graphene.String()
    size_x = graphene.Int()
    size_y = graphene.Int()
    connections = graphene.List(graphene.String)


class QuestType(graphene.ObjectType):
    name = graphene.String()
    completed = graphene.Boolean()
    description = graphene.String()


class EffectType(graphene.ObjectType):
    target_attributes = graphene.List(graphene.String)
    duration = graphene.Int()
    value = graphene.Float()
    condition = graphene.String()


class ItemType(graphene.ObjectType):
    name = graphene.String()
    kind = graphene.String()
    effect = graphene.Field(EffectType)
    count = graphene.Int()
    description = graphene.String()
    buy_price = graphene.Int()
    sell_price = graphene.Int()


class SkillType(graphene.ObjectType):
    skill_id = graphene.Int()
    name = graphene.String()
    sp_cost = graphene.Int()
    power = graphene.Int()
    range = graphene.Int()
    description = graphene.String()
    classes = graphene.List(graphene.String)
    ep_cost = graphene.Int()


class EquipmentType(graphene.ObjectType):
    head = graphene.Field(ItemType)
    torso = graphene.Field(ItemType)
    legs = graphene.Field(ItemType)
    weapon = graphene.Field(ItemType)
    shield = graphene.Field(ItemType)
    accessory_1 = graphene.Field(ItemType)
    accessory_2 = graphene.Field(ItemType)


class WalletType(graphene.ObjectType):
    copper_coins = graphene.Int()
    silver_coins = graphene.Int()
    gold_coins = graphene.Int()


class CharacterType(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    lv = graphene.Int()
    next_lv = graphene.Int()
    exp = graphene.Int()
    max_hp = graphene.Int()
    max_sp = graphene.Int()
    current_hp = graphene.Int()
    current_sp = graphene.Int()
    power = graphene.Int()
    resistance = graphene.Int()
    agility = graphene.Int()
    is_ko = graphene.Boolean()
    is_logged = graphene.Boolean()
    last_activity = graphene.DateTime()
    position_x = graphene.Int()
    position_y = graphene.Int()
    area_location = graphene.String()
    items = DynamicScalar()
    equipment = graphene.List(DynamicScalar)
    skills = graphene.List(graphene.Int)
    quests = graphene.List(QuestType)
    class_type = graphene.String()
    effects = graphene.List(EffectType)
    aim = graphene.Int()
    wallet = graphene.Int()
    ep = graphene.Int()
    equipped_skill = graphene.Int()
    equipped_item = graphene.Int()
    map_metadata = graphene.Field(MapAreaType)

    def resolve_map_metadata(self, info, **kwargs):
        return areas[self.area_location]

    def resolve_skills(self, info, **kwargs):
        return json.loads(self.skills.decode('utf-8'))

    def resolve_items(self, info, **kwargs):
        return self.getItems()

    def resolve_effects(self, info, **kwargs):
        return json.loads(self.effects.decode('utf-8'))

    def resolve_equipment(self, info, **kwargs):
        return json.loads(self.equipment.decode('utf-8'))

    def resolve_quests(self, info, **kwargs):
        return json.loads(self.quests.decode('utf-8'))


class EnemyType(graphene.ObjectType):
    lv = graphene.Int()
    name = graphene.String()
    max_hp = graphene.Int()
    power = graphene.Int()
    resistance = graphene.Int()
    agility = graphene.Int()
    aim = graphene.Int()
    class_type = graphene.String()
    exp = graphene.Int()
    drops = graphene.List(ItemType)
    skills = graphene.List(SkillType)

    def resolve_drops(self, info, **kwargs):
        return json.loads(self.drops.decode('utf-8'))

    def resolve_skills(self, info, **kwargs):
        return json.loads(self.skills.decode('utf-8'))


class ItemOfferInputType(graphene.InputObjectType):
    name = graphene.String()
    count = graphene.Int()


class ItemBatchOfferType(graphene.ObjectType):
    id = graphene.ID()
    price = graphene.Field(WalletType)
    seller = graphene.Field(CharacterType)
    items = graphene.List(ItemType)

    def resolve_items(self, info, **kwargs):
        return self.getItems()
    
    def resolve_price(self, info, **kwargs):
        return {
            'copper_coins': self.price % 100,
            'silver_coins': (self.price // 100) % 100,
            'gold_coins': self.price // 10000
        }


class EnemiesSpawnedType(EnemyType):
    id = graphene.ID()
    area_location = graphene.String()
    current_hp = graphene.Int()
    effects = graphene.List(EffectType)
    is_ko = graphene.Boolean()
    position_x = graphene.Int()
    position_y = graphene.Int()

    def resolve_effects(self, info, **kwargs):
        return json.loads(self.effects.decode('utf-8'))


##########################
# Query
##########################
class Query:

    # API Version
    version = graphene.String(
        description='Returns service version'
    )
    def resolve_version(self, info, **kwargs):
        return settings.VERSION

    # Chat History
    history = graphene.List(Message, chatroom=graphene.String())
    def resolve_history(self, info, chatroom):
        """Return chat history."""
        del info
        return chats[chatroom] if chatroom in chats else []

    # Characters
    # TODO filters
    characters = graphene.List(
        CharacterType,
        is_logged=graphene.Boolean(required=True),
        area_location=graphene.String(required=True)
    )
    def resolve_characters(self, info, **kwargs):
        return Character.objects.filter(**kwargs)

    character = graphene.Field(
        CharacterType,
        id=graphene.ID(required=True)
    )
    def resolve_character(self, info, **kwargs):
        return Character.objects.get(id=kwargs['id'])

    # Skills
    skills = graphene.List(SkillType)
    def resolve_skills(self, info, **kwargs):
        return skill_list.values()

    # Map areas
    map_areas = graphene.List(MapAreaType)
    def resolve_map_areas(self, info, **kwargs):
        return areas.values()

    map_area = graphene.Field(
        MapAreaType,
        name=graphene.String(required=True)
    )
    def resolve_map_area(self, info, **kwargs):
        return areas.get(kwargs['name'])

    # Enemies
    enemies = graphene.List(EnemyType)
    def resolve_enemies(self, info, **kwargs):
        return enemy_list.values()

    # Enemy
    enemy = graphene.Field(
        EnemyType,
        name=graphene.String(required=True)
    )
    def resolve_enemy(self, info, **kwargs):
        return enemy_list.get(kwargs['name'])
    
    # Items
    items = graphene.List(ItemType)
    def resolve_items(self, info, **kwargs):
        return item_list.values()

    # Item
    item = graphene.Field(
        ItemType,
        name=graphene.String(required=True)
    )
    def resolve_item(self, info, **kwargs):
        return item_list.get(kwargs['name'])
    
    # Item offers
    offers = graphene.List(ItemBatchOfferType)
    def resolve_offers(self, info, **kwargs):
        return ItemOffer.objects.filter(**kwargs)
    
    # Item offer
    offer = graphene.Field(
        ItemBatchOfferType,
        id=graphene.ID(required=True)
    )
    def resolve_offer(self, info, **kwargs):
        return ItemOffer.objects.get(id=kwargs['id'])

    # Enemies spawned
    enemies_spawned = graphene.List(
        EnemiesSpawnedType,
        area_location=graphene.String()
    )
    def resolve_enemies_spawned(self, info, **kwargs):
        return SpawnedEnemy.objects.filter(**kwargs)


##########################
# Mutation
##########################
class SendChatMessage(graphene.Mutation, name="SendChatMessagePayload"):  # type: ignore
    """Send chat message."""

    ok = graphene.Boolean()

    class Arguments:
        """Mutation arguments."""

        id = graphene.ID()
        chatroom = graphene.String()
        text = graphene.String()

    def mutate(self, info, chatroom, text, **kwargs):
        """Mutation "resolver" - store and broadcast a message."""

        sender = kwargs.get('user')

        # Store a message.
        chats[chatroom].append({"id": kwargs['id'], "chatroom": chatroom, "text": text, "sender": sender})

        # Notify subscribers.
        OnNewChatMessage.new_chat_message(id=kwargs['id'], chatroom=chatroom, text=text, sender=sender)

        return SendChatMessage(ok=True)


class CreateCharacter(graphene.relay.ClientIDMutation):
    character = graphene.Field(CharacterType)

    class Input:
        name = graphene.String(required=True)
        character_class = ChracterClass(required=True)
        username = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate_and_get_payload(self, info, **kwargs):
        try:
            user = User.objects.get(
                username=kwargs['username'],
                email=kwargs['email']
            )
        except User.DoesNotExist:
            raise Exception('Invalid user profile')

        try:
            character = Character.objects.create(
                name=kwargs['name'],
                class_type=kwargs['character_class'],
                user=user
            )
        except Exception as ex:
            print(ex)
            raise Exception('Failed to create the character')

        # set base skills
        character.skills = json.dumps([]).encode('utf-8')

        # Set item bag
        character.items = json.dumps({}).encode('utf-8')

        # Set equipments
        equipment = [
            {'_dataClass': 'weapon', '_itemId': 0},
            {'_dataClass': '', '_itemId': 0},
            {'_dataClass': 'armor', '_itemId': 0},
            {'_dataClass': 'armor', '_itemId': 0},
            {'_dataClass': '', '_itemId': 0},
        ]
        character.equipment = json.dumps(equipment).encode('utf-8')

        # Set quests
        character.quests = json.dumps({}).encode('utf-8')

        # Set effects (status ailments)
        character.effects = json.dumps([]).encode('utf-8')

        # Add class bonus attributes
        bonus_attrs = classes[kwargs['character_class']]
        character.max_hp += bonus_attrs['hp']
        character.max_sp += bonus_attrs['sp']
        character.current_hp += bonus_attrs['hp']
        character.current_sp += bonus_attrs['sp']
        character.power += bonus_attrs['power']
        character.resistance += bonus_attrs['resistance']
        character.agility += bonus_attrs['agility']

        character.save()

        return CreateCharacter(character)


class LocationInput(graphene.InputObjectType):
    x = graphene.Int(required=True)
    y = graphene.Int(required=True)


class UpdatePosition(graphene.relay.ClientIDMutation):
    character = graphene.Field(CharacterType)

    class Input:
        id = graphene.ID(required=True)
        location = graphene.Argument(LocationInput, required=True)

    # @access_required
    def mutate_and_get_payload(self, info, **kwargs):
        location = kwargs.get('location')
        x = location.get('x')
        y = location.get('y')
        character_id = kwargs.get('id')

        char = Character.objects.get(
            # user=kwargs.get('user'),
            id=character_id
        )
        # if not target_position_is_valid([x, y], char.area_location):
        #     raise Exception('Invalid location')
        char.position_x = x
        char.position_y = y
        char.save()

        payload = {
            'id': char.id,
            'name': char.name,
            'x': char.position_x,
            'y': char.position_y,
            'map_area': char.area_location
        }
        OnCharacterEvent.char_event(params={
            'event_type': 'character_movement',
            'data': payload
        })

        return UpdatePosition(char)


class UpdateEnemyPosition(graphene.relay.ClientIDMutation):
    enemy = graphene.Field(EnemiesSpawnedType)

    class Input:
        id = graphene.ID(required=True)
        location = graphene.Argument(LocationInput, required=True)

    # @access_required
    def mutate_and_get_payload(self, info, **kwargs):
        location = kwargs.get('location')
        x = location.get('x')
        y = location.get('y')
        enemy_id = kwargs.get('id')

        enemy = SpawnedEnemy.objects.get(
            # user=kwargs.get('user'),
            id=enemy_id
        )
        # if not target_position_is_valid([x, y], enemy.area_location):
        #     raise Exception('Invalid location')
        enemy.position_x = x
        enemy.position_y = y
        enemy.save()

        payload = {
            'id': enemy.id,
            'name': enemy.name,
            'x': enemy.position_x,
            'y': enemy.position_y,
            'map_area': enemy.area_location
        }
        OnCharacterEvent.char_event(params={
            'event_type': 'enemy_movement',
            'data': payload
        })

        return UpdateEnemyPosition(enemy)


class CharacterLogIn(graphene.relay.ClientIDMutation):
    """Enters the game with a selected character"""
    
    character = graphene.Field(CharacterType)

    class Input:
        id = graphene.ID(required=True)

    # @access_required
    def mutate_and_get_payload(self, info, **kwargs):
        # user = kwargs.get('user')
        # if not user:
        #     raise Exception('Unauthorized!')

        # Try recover the Character
        try:
            char = Character.objects.get(
                # user=user,
                id=kwargs['id']
            )
        except Character.DoesNotExist:
            raise Exception('Invalid character!')

        # Good to go
        char.is_logged = True
        char.save()

        # Broadcast character login
        OnCharacterEvent.char_event(params={
            'event_type': 'character_login',
            'data': CharacterPublishPayload.get_player_payload(
                'character_login',
                char
            )
        })

        return CharacterLogIn(char)


class CharacterLogOut(graphene.relay.ClientIDMutation):
    """Leaves the game with a selected character"""
    
    log_status = graphene.Boolean()

    class Input:
        id = graphene.ID(required=True)

    # @access_required
    def mutate_and_get_payload(self, info, **kwargs):
        # user = kwargs.get('user')
        # if not user:
        #     raise Exception('Unauthorized!')

        # Try recover the Character
        try:
            char = Character.objects.get(
                # user=user,
                id=kwargs['id']
            )
        except Character.DoesNotExist:
            raise Exception('Invalid character!')

        # Good to go
        char.is_logged = False
        char.save()

        # Broadcast character logout
        OnCharacterEvent.char_event(params={
            'event_type': 'character_logout',
            'data': CharacterPublishPayload.get_player_payload(
                'character_logout',
                char
            )
        })

        return CharacterLogIn(True)


class CharacterUseSkill(graphene.relay.ClientIDMutation):
    result = graphene.Boolean()

    class Input:
        skill_user_id = graphene.ID(required=True)
        skill_id = graphene.ID(required=True)
        direction = graphene.Int(required=True)
        class_type = graphene.String(required=True)
 
    def mutate_and_get_payload(self, info, **kwargs):
        if kwargs['class_type'] == 'enemy':
            try:
                skill_user = Character.objects.get(id=kwargs['skill_user_id'])
            except (SpawnedEnemy.DoesNotExist):
                raise Exception('Invalid character')

        else:
            try:
                skill_user = Character.objects.get(id=kwargs['skill_user_id'])
            except Character.DoesNotExist:
                raise Exception('Invalid character')

        OnCharacterEvent.char_event(params={
            'event_type': 'use_skill',
            'data': CharacterPublishPayload.get_player_payload(
                'use_skill',
                skill_user,
                skill_id=kwargs['skill_id'],
                direction=kwargs['direction']
            )
        })

        return CharacterUseSkill(True)

   
class CharacterUpdateItem(graphene.relay.ClientIDMutation):
    character = graphene.Field(CharacterType)
    
    class Input:
        character_id = graphene.ID(required=True)
        item_data = graphene.String(required=True)
        count = graphene.Int(required=True)
        
    def mutate_and_get_payload(self, info, **kwargs):
        try:
            character = Character.objects.get(id=kwargs['character_id'])
        except Character.DoesNotExist:
            raise Exception('Invalid character')
        
        try:
            item_data = json.loads(
                b64decode(kwargs['item_data'].encode('utf-8')).decode('utf-8')
            )
        except:
            raise Exception('Invalid item data')

        count = kwargs['count']
        if count == 0:
            raise Exception('Invalid amount')

        # if item_name not in item_list:
        #     raise Exception('Invalid item')
        
        char_items = character.getItems()

        if item_data.get('name') in char_items:
            char_items[item_data.get('name')]['count'] += count
        else:
            char_items[item_data.get('name')] = {
                'data': item_data,
                'count': count
            }
            
        if char_items[item_data.get('name')]['count'] <= 0:
            char_items.pop(item_data.get('name'))
            
        character.setItems(char_items)
        character.save()

        return CharacterUpdateItem(character)


class CharacterUseItem(graphene.relay.ClientIDMutation):
    character = graphene.Field(CharacterType)

    class Input:
        character_id = graphene.ID()
        item_name = graphene.String()

    def mutate_and_get_payload(self, info, **kwargs):
        try:
            character = Character.objects.get(id=kwargs['character_id'])
        except Character.DoesNotExist:
            raise Exception('Invalid character')
        
        item_name = kwargs['item_name']
        if item_name not in item_list:
            raise Exception('Invalid item')
        
        char_items = character.getItems()
        
        if item_name not in char_items.keys():
            raise Exception("You don't have any of this item!")
        
        item = char_items[item_name]
        
        if item['count'] <= 0:
            raise Exception("You don't have any of this item!")
        
        # use item
        item['count'] -= 1
        item.use()
        
        if item['count'] <= 0:
            char_items.pop(item_name)
            
        character.setItems(char_items)
        character.save()

        return CharacterUseItem(character)


class CharacterSellItem(graphene.relay.ClientIDMutation):
    character = graphene.Field(CharacterType)
    
    class Input:
        character_id = graphene.ID(required=True)
        item_name = graphene.String(required=True)
        count = graphene.Int(required=True)
        
    def mutate_and_get_payload(self, info, **kwargs):
        try:
            character = Character.objects.get(id=kwargs['character_id'])
        except Character.DoesNotExist:
            raise Exception('Invalid character')
        
        item_name = kwargs['item_name']
        count = kwargs['count']
        
        if item_name not in item_list:
            raise Exception('Invalid item')
        
        char_items = character.getItems()
        
        if item_name not in char_items.keys():
            raise Exception("You don't have any of this item to sell")
        
        item = char_items[item_name]
        
        if count <= 0:
            raise Exception("Invalid amount")
        if count > item['count']:
            raise Exception("You don't have enough of this item to sell")
        
        character.wallet += item['sell_price'] * count
        
        item['count'] -= count    
        if item['count'] <= 0:  
            char_items.pop(item_name)
            
        character.setItems(char_items)
        character.save()

        return CharacterSellItem(character)


class CharacterBuyItem(graphene.relay.ClientIDMutation):
    character = graphene.Field(CharacterType)
    
    class Input:
        character_id = graphene.ID(required=True)
        item_name = graphene.String(required=True)
        count = graphene.Int(required=True)
        
    def mutate_and_get_payload(self, info, **kwargs):
        try:
            character = Character.objects.get(id=kwargs['character_id'])
        except Character.DoesNotExist:
            raise Exception('Invalid character')
        
        item_name = kwargs['item_name']
        count = kwargs['count']
        
        if item_name not in item_list:
            raise Exception('Invalid item')
        
        char_items = character.getItems()
        
        if item_name in char_items.keys():
            item = char_items[item_name]
        else:
            item = item_list[item_name].copy()
            item['count'] = 0
            
        buy_price = item['buy_price'] * count
        if character.wallet < buy_price:
            raise Exception("You don't have enough money to buy this item")
            
        character.wallet -= buy_price
        item['count'] += count

        if item_name not in char_items.keys():
            char_items[item_name] = item
            
        character.setItems(char_items)
        character.save()

        return CharacterBuyItem(character)


class CharacterBatchSellOffer(graphene.relay.ClientIDMutation):
    batch_offer = graphene.Field(ItemBatchOfferType)

    class Input:
        character_id = graphene.ID(required=True)
        copper_price = graphene.Int(default=0)
        silver_price = graphene.Int(default=0)
        gold_price = graphene.Int(default=0)
        items = graphene.List(ItemOfferInputType, required=True)
    
    def mutate_and_get_payload(self, info, **kwargs):
        try:
            character = Character.objects.get(id=kwargs['character_id'])
        except Character.DoesNotExist:
            raise Exception("Invalid character")
        
        copper_price = kwargs.get('copper_price', 0)
        silver_price = kwargs.get('silver_price', 0)
        gold_price = kwargs.get('gold_price', 0)
        
        if  (copper_price < 0) or (copper_price > GAME_CONFIG['MAX_COPPER_COINS']) or\
            (silver_price < 0) or (silver_price > GAME_CONFIG['MAX_SILVER_COINS']) or\
            (gold_price < 0) or (gold_price > GAME_CONFIG['MAX_GOLD_COINS']):
                raise Exception('Invalid coin amounts')
        price = copper_price + 100*silver_price + 10000*gold_price

        char_items = character.getItems()
        item_input = {i['name']: i['count'] for i in kwargs['items']}
        items = [i.copy() for i in char_items.values() if i['name'] in item_input]
        
        if len(items) == 0:
            raise Exception('No valid items were provided')
        
        for i in items:
            i['count'] = item_input[i['name']]
            player_count = char_items[i['name']]['count']
            if i['count'] <= 0:
                raise Exception(f'Invalid item count of {i["name"]}') 
            if player_count < i['count']:
                raise Exception(f'Character doesn\'t have enough of {i["name"]}')
            
        for i in items:
            char_items[i['name']]['count'] -= i['count']
        
        offer = ItemOffer.objects.create(
            seller=character,
            price=price
        )
        print(items)
        offer.setItems(items)
        character.setItems(char_items)
        character.save()
        offer.save()
        
        # Broadcast offer available
        payload = {
            'id': offer.id,
            'seller_id': character.id,
            'price': {
                'copper_coins': price % 100,
                'silver_coins': (price // 100) % 100,
                'gold_coins': price // 10000
            },
            'items': [{
                'id': item['name'],
                'count': item['count']
            } for item in offer.getItems()]
        }
        OnCharacterEvent.char_event(params={
            'event_type': 'offer_available',
            'data': payload
        })
        
        return CharacterBatchSellOffer(offer)
    

class CharacterBatchBuyOffer(graphene.relay.ClientIDMutation):
    character = graphene.Field(CharacterType)

    class Input:
        character_id = graphene.ID(required=True)
        offer_id = graphene.ID(required=True)
    
    def mutate_and_get_payload(self, info, **kwargs):
        try:
            character = Character.objects.get(id=kwargs['character_id'])
            offer = ItemOffer.objects.get(id=kwargs['offer_id'])
        except Character.DoesNotExist:
            raise Exception("Invalid character")
        except ItemOffer.DoesNotExist:
            raise Exception("Invalid offer")
        
        if character == offer.seller:
            raise Exception("Player cannot buy from itself")
    
        if character.wallet < offer.price:
            raise Exception("Character doesn't have enough money")
        
        char_items = character.getItems()
        offer_items = offer.getItems()
        for item in offer_items:
            if item['name'] in char_items.keys():
                char_items[item['name']]['count'] += item['count']
            else:
                char_items[item['name']] = item.copy()
        
        character.wallet -= offer.price
        offer.seller.wallet += offer.price

        offer.seller.save()
        character.setItems(char_items)
        character.save()
        
        # Broadcast offer accepted
        payload = {
            'buyer': {
                'id': character.id,
                'wallet': {
                    'copper_coins': character.wallet % 100,
                    'silver_coins': (character.wallet // 100) % 100,
                    'gold_coins': character.wallet // 10000
                }
            },
            'seller': {
                'id': offer.seller.id,
                'wallet': {
                    'copper_coins': offer.seller.wallet % 100,
                    'silver_coins': (offer.seller.wallet // 100) % 100,
                    'gold_coins': offer.seller.wallet // 10000
                }
            }
        }
        OnCharacterEvent.char_event(params={
            'event_type': 'offer_accepted',
            'data': payload
        })

        offer.delete()
        
        return CharacterBatchBuyOffer(character)


class CharacterBatchRevokeOffer(graphene.relay.ClientIDMutation):
    character = graphene.Field(CharacterType)

    class Input:
        character_id = graphene.ID(required=True)
        offer_id = graphene.ID(required=True)
    
    def mutate_and_get_payload(self, info, **kwargs):
        try:
            character = Character.objects.get(id=kwargs['character_id'])
            offer = ItemOffer.objects.get(id=kwargs['offer_id'])
        except Character.DoesNotExist:
            raise Exception("Invalid character")
        except ItemOffer.DoesNotExist:
            raise Exception("Invalid offer")
        
        if character != offer.seller:
            raise Exception("Only seller can revoke the offer")
    
        char_items = character.getItems()
        offer_items = offer.getItems()
        for item in offer_items:
            if item['name'] in char_items.keys():
                char_items[item['name']]['count'] += item['count']
            else:
                char_items[item['name']] = item.copy()
        
        offer.delete()
        character.setItems(char_items)
        character.save()
        
        return CharacterBatchBuyOffer(character)


class CharacterMapAreaTransfer(graphene.relay.ClientIDMutation):
    character = graphene.Field(CharacterType)

    class Input:
        id = graphene.ID(required=True)
        area_name = graphene.String(required=True)

    def mutate_and_get_payload(self, info, **kwargs):
        try:
            character = Character.objects.get(id=kwargs['id'])
        except Character.DoesNotExist:
            raise Exception('Character not found')

        current_area = character.area_location
        target_area = kwargs['area_name']

        if current_area == target_area:
            raise Exception('Cannot transfer to same area')

        if not target_area in areas[current_area]['connections']:
            raise Exception('Cannot move to the requested area from current area')

        x, y = area_transfer_coord_map[current_area][target_area]

        character.area_location = target_area
        character.position_x = x
        character.position_y = y
        character.save()

        # Broadcast character area transfer
        OnCharacterEvent.char_event(params={
            'event_type': 'area_transfer',
            'data': CharacterPublishPayload.get_player_payload(
                'area_transfer',
                character,
                from_map=current_area,
                to_area=character.area_location
            )
        })

        return CharacterMapAreaTransfer(character)


class NotifyEnemyEvent(graphene.relay.ClientIDMutation):
    result = graphene.Boolean()

    class Input:
        event_type = graphene.String(required=True)
        data = graphene.String(required=True)

    def mutate_and_get_payload(self, info, **kwargs):
        data = json.loads(b64decode(kwargs['data'].encode('utf-8').decode('utf-8')))
        event_type = kwargs['event_type']

        OnCharacterEvent.char_event(params={
            'event_type': event_type,
            'data': data
        })
        return NotifyEnemyEvent(True)


class SetCharactertRespawnSpot(graphene.relay.ClientIDMutation):
    character = graphene.Field(CharacterType)

    class Input:
        id = graphene.ID(required=True)
        spot = graphene.String(requred=True)

    def mutate_and_get_payload(self, info, **kwargs):
        try:
            character = Character.objects.get(id=kwargs['id'])
        except Character.DoesNotExist:
            raise Exception('Invalid character')

        if kwargs['spot'] not in RespawnSpots.spots:
            raise Exception('Invalid spot')

        character.respawn_spot = kwargs['spot']
        character.save()

        return SetCharactertRespawnSpot(character)


class CharacterRespawn(graphene.relay.ClientIDMutation):
    character = graphene.Field(CharacterType)

    class Input:
        id = graphene.ID(required=True)

    def mutate_and_get_payload(self, info, **kwargs):
        try:
            character = Character.objects.get(id=kwargs['id'])
        except Character.DoesNotExist:
            raise Exception('Invalid character')

        x, y =  choice(RespawnSpots.spots[character.respawn_spot])

        character.position_x = x
        character.position_y = y

        current_area = character.area_location
        character.is_ko = False
        character.current_hp = character.max_hp
        character.current_sp = character.max_sp
        character.area_location = character.respawn_spot
        character.save()

        # Broadcast the area transfer when respawn to re-render character sprite
        OnCharacterEvent.char_event(params={
            'event_type': 'area_transfer',
            'data': CharacterPublishPayload.get_player_payload(
                'area_transfer',
                character,
                from_map=current_area,
                to_area=character.area_location
            )
        })

        return CharacterRespawn(character)


class LearnSkill(graphene.relay.ClientIDMutation):
    character = graphene.Field(CharacterType)

    class Input:
        skill_id = graphene.Int(required=True)
        character_id = graphene.ID(required=True)

    def mutate_and_get_payload(self, info, **kwargs):
        try:
            character = Character.objects.get(id=kwargs['character_id'])
        except Character.DoesNotExist:
            raise Exception('Character not found')

        char_skills = json.loads(character.skills.decode('utf-8'))

        if kwargs['skill_id'] in char_skills:
            raise Exception('Skill aready learned by this character')

        skill = None
        for skill_data in skill_list.values():
            if kwargs['skill_id'] == skill_data['skill_id']:
                skill = skill_data
                break

        if not skill:
            raise Exception('Invalid skill')

        if character.class_type not in skill['classes']:
            raise Exception('Cannot learn this skill')

        if skill['ep_cost'] > character.ep:
            raise Exception('Not enough Evolution Points')

        # All checked, learn the skill
        character.ep -= skill['ep_cost']
        char_skills.append(skill['skill_id'])
        character.skills = json.dumps(char_skills).encode('utf-8')
        character.save()

        return LearnSkill(character)


class UpdateCharacterVitalStats(graphene.relay.ClientIDMutation):
    character = graphene.Field(CharacterType)

    class Input:
        id = graphene.ID(required=True)
        hp = graphene.Int(required=True)
        sp = graphene.Int(required=True)

    def mutate_and_get_payload(self, info, **kwargs):
        try:
            character = Character.objects.get(id=kwargs['id'])
        except Character.DoesNotExist:
            raise Exception('Invalid character')

        character.current_hp = kwargs['hp'] if kwargs['hp'] < character.max_hp else character.max_hp
        character.current_sp = kwargs['sp'] if kwargs['sp'] < character.max_sp else character.max_sp

        if character.current_hp <= 0:
            character.is_ko = True

        character.save()

        OnCharacterEvent.char_event(params={
            'event_type': 'character_health',
            'data': CharacterPublishPayload.get_player_payload(
                'character_health',
                character
            )
        })

        return UpdateCharacterVitalStats(character)


class UpdateEnemyVitalStats(graphene.relay.ClientIDMutation):
    enemy = graphene.Field(EnemiesSpawnedType)

    class Input:
        id = graphene.ID(required=True)
        hp = graphene.Int(required=True)
        sp = graphene.Int(required=True)

    def mutate_and_get_payload(self, info, **kwargs):
        try:
            enemy = SpawnedEnemy.objects.get(id=kwargs['id'])
        except SpawnedEnemy.DoesNotExist:
            raise Exception('Invalid enemy')

        enemy_id = enemy.id  # store enemy ID in case of KO
        enemy.current_hp = kwargs['hp'] if kwargs['hp'] < enemy.max_hp else enemy.max_hp
        enemy.current_sp = kwargs['sp'] if kwargs['sp'] < enemy.max_sp else enemy.max_sp

        if enemy.current_hp <= 0:
            enemy.is_ko = True
            enemy.delete()
        else:
            enemy.save()

        # Broadcast enemy health
        payload = {
            'id': enemy_id,
            'name': enemy.name,
            'x': enemy.position_x,
            'y': enemy.position_y,
            'map_area': enemy.area_location,
            'classType': 'enemy',
            'hp': enemy.current_hp,
            'is_ko': enemy.is_ko
        }
        OnCharacterEvent.char_event(params={
            'event_type': 'enemy_health',
            'data': payload
        })

        return UpdateEnemyVitalStats(enemy)


class GainExp(graphene.relay.ClientIDMutation):
    character = graphene.Field(CharacterType)

    class Input:
        id = graphene.ID(required=True)
        exp = graphene.Int(required=True)
        is_lv_up = graphene.Boolean(required=True)
        lv = graphene.Int(required=True)
        max_hp = graphene.Int(required=True)
        max_sp = graphene.Int(required=True)
        power = graphene.Int(required=True)
        resistance = graphene.Int(required=True)
        agility = graphene.Int(required=True)

    def mutate_and_get_payload(self, info, **kwargs):
        try:
            character = Character.objects.get(id=kwargs['id'])
        except Character.DoesNotExist:
            raise Exception('Character not found')

        character.exp += kwargs['exp']
        if kwargs['is_lv_up']:
            character.lv = kwargs['lv']
            character.max_hp = kwargs['max_hp']
            character.max_sp = kwargs['max_sp']
            character.power = kwargs['power']
            character.resistance = kwargs['resistance']
            character.agility = kwargs['agility']
            character.ep += 3
        character.save()

        return GainExp(character)


class GainGold(graphene.relay.ClientIDMutation):
    character = graphene.Field(CharacterType)

    class Input:
        id = graphene.ID(required=True)
        amount = graphene.Int(required=True)

    def mutate_and_get_payload(self, info, **kwargs):
        try:
            character = Character.objects.get(id=kwargs['id'])
        except Character.DoesNotExist:
            raise Exception('Character not found')

        if (kwargs['amount'] + character.wallet) < 0:
            raise Exception('Not enought gold!')

        character.wallet += kwargs['amount']
        character.save()

        return GainGold(character)


class UpdateEquipment(graphene.relay.ClientIDMutation):
    character = graphene.Field(CharacterType)

    class Input:
        character_id = graphene.ID(required=True)
        equipment_data = graphene.String(required=True)

    def mutate_and_get_payload(self, info, **kwargs):
        try:
            character = Character.objects.get(id=kwargs['character_id'])
        except Character.DoesNotExist:
            raise Exception('Character not found')

        try:
            equipment = json.loads(
                b64decode(kwargs['equipment_data'].encode('utf-8')).decode('utf-8')
            )
        except:
            raise Exception('Invalid quipment data')

        character.equipment = json.dumps(equipment).encode('utf-8')
        character.save()

        return UpdateEquipment(character)


class EquipSkill(graphene.relay.ClientIDMutation):
    character = graphene.Field(CharacterType)

    class Input:
        character_id = graphene.ID(required=True)
        skill_id = graphene.Int(required=True)

    def mutate_and_get_payload(self, info, **kwargs):
        try:
            character = Character.objects.get(id=kwargs['character_id'])
        except Character.DoesNotExist:
            raise Exception('Character not found')

        char_skills = json.loads(character.skills.decode('utf-8'))
        if kwargs['skill_id'] not in char_skills:
            raise Exception('Cannot equip unlearned or invalid skill')

        character.equipped_skill = kwargs['skill_id']
        character.save()
        return EquipSkill(character)


class EquipItem(graphene.relay.ClientIDMutation):
    character = graphene.Field(CharacterType)

    class Input:
        character_id = graphene.ID(required=True)
        item_id = graphene.Int(required=True)

    def mutate_and_get_payload(self, info, **kwargs):
        try:
            character = Character.objects.get(id=kwargs['character_id'])
        except Character.DoesNotExist:
            raise Exception('Character not found')

        # TODO validate if player has the requested item
        # char_skills = json.loads(character.skills.encode('utf-8'))
        # if kwargs['skill_id'] not in char_skills:
        #     raise Exception('Cannot equip unlearned or invalid skill')

        character.equipped_item = kwargs['item_id']
        character.save()
        return EquipItem(character)


class Mutation:
    send_chat_message = SendChatMessage.Field()
    create_character = CreateCharacter.Field()
    update_position = UpdatePosition.Field()
    character_login = CharacterLogIn.Field()
    character_logout = CharacterLogOut.Field()
    character_use_skill = CharacterUseSkill.Field()
    character_update_item = CharacterUpdateItem.Field()
    character_use_item = CharacterUseItem.Field()
    character_buy_item = CharacterBuyItem.Field()
    character_sell_item = CharacterSellItem.Field()
    character_batch_sell_offer = CharacterBatchSellOffer.Field()
    character_batch_buy_offer = CharacterBatchBuyOffer.Field()
    character_batch_revoke_offer = CharacterBatchRevokeOffer.Field()
    character_map_area_transfer = CharacterMapAreaTransfer.Field()
    notify_enemy_event = NotifyEnemyEvent.Field()
    character_respawn = CharacterRespawn.Field()
    learn_skill = LearnSkill.Field()
    update_enemy_position = UpdateEnemyPosition.Field()
    update_character_vital_stats = UpdateCharacterVitalStats.Field()
    update_enemy_vital_stats = UpdateEnemyVitalStats.Field()
    set_character_respawn_spot = SetCharactertRespawnSpot.Field()
    gain_exp = GainExp.Field()
    gain_gold = GainGold.Field()
    update_equipment = UpdateEquipment.Field()
    equip_skill = EquipSkill.Field()
    equip_item = EquipItem.Field()


#################
# SUBSCRIPTIONS
#################


class OnNewChatMessage(channels_graphql_ws.Subscription):
    """Subscription triggers on a new chat message."""

    id = graphene.ID()
    sender = graphene.String()
    chatroom = graphene.String()
    text = graphene.String()

    class Arguments:
        """Subscription arguments."""

        chatroom = graphene.String()

    def subscribe(self, info, chatroom=None):
        """Client subscription handler."""
        del info
        # Specify the subscription group client subscribes to.
        return [chatroom] if chatroom is not None else None

    def publish(self, info, chatroom=None):
        """Called to prepare the subscription notification message."""

        # The `self` contains payload delivered from the `broadcast()`.
        new_msg_id = self["id"]
        new_msg_chatroom = self["chatroom"]
        new_msg_text = self["text"]
        new_msg_sender = self["sender"]

        # Method is called only for events on which client explicitly
        # subscribed, by returning proper subscription groups from the
        # `subscribe` method. So he either subscribed for all events or
        # to particular chatroom.
        assert chatroom is None or chatroom == new_msg_chatroom

        # Avoid self-notifications.
        if (
            info.context.user.is_authenticated
            and new_msg_sender == info.context.user.username
        ):
            return OnNewChatMessage.SKIP

        return OnNewChatMessage(
            id=new_msg_id, chatroom=chatroom, text=new_msg_text, sender=new_msg_sender
        )

    @classmethod
    def new_chat_message(cls, id, chatroom, text, sender):
        """Auxiliary function to send subscription notifications.
        It is generally a good idea to encapsulate broadcast invocation
        inside auxiliary class methods inside the subscription class.
        That allows to consider a structure of the `payload` as an
        implementation details.
        """
        print(id)
        cls.broadcast(
            group=chatroom,
            payload={"id": id, "chatroom": chatroom, "text": text, "sender": sender},
        )
        

class Subscription(graphene.ObjectType):
    """GraphQL subscriptions."""

    on_new_chat_message = OnNewChatMessage.Field()
    on_character_event = OnCharacterEvent.Field()
