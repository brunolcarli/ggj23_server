import json
from collections import defaultdict
import channels_graphql_ws
from ast import literal_eval
from site import ENABLE_USER_SITE
import graphene
from graphql import GraphQLObjectType
from django.conf import settings
from django.contrib.auth.models import User
from server_app.models import Character
from server_app.skills import skill_list
from server_app.map_areas import areas
from server_app.character_classes import classes, ChracterClass
from server_app.engine import target_position_is_valid

chats = defaultdict(list)


class Message(  # type: ignore
    graphene.ObjectType, default_resolver=graphene.types.resolver.dict_resolver
):
    """Message GraphQL type."""

    chatroom = graphene.String()
    text = graphene.String()
    sender = graphene.String()


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


class SkillType(graphene.ObjectType):
    name = graphene.String()
    sp_cost = graphene.Int()
    power = graphene.Int()
    range = graphene.Int()
    effect = graphene.Field(EffectType)
    description = graphene.String()
    classes = graphene.List(graphene.String)


class EquipmentType(graphene.ObjectType):
    head = graphene.Field(ItemType)
    torso = graphene.Field(ItemType)
    legs = graphene.Field(ItemType)
    weapon = graphene.Field(ItemType)
    shield = graphene.Field(ItemType)
    accessory_1 = graphene.Field(ItemType)
    accessory_2 = graphene.Field(ItemType)


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
    items = graphene.List(ItemType)
    equipment = graphene.Field(EquipmentType)
    skills = graphene.List(SkillType)
    quests = graphene.List(QuestType)
    class_type = graphene.String()
    effects = graphene.List(EffectType)
    aim = graphene.Int()

    def resolve_skills(self, info, **kwargs):
        return json.loads(self.skills.decode('utf-8')).values()

    def resolve_items(self, info, **kwargs):
        return json.loads(self.items.decode('utf-8')).values()

    def resolve_effects(self, info, **kwargs):
        return json.loads(self.effects.decode('utf-8'))

    def resolve_equipment(self, info, **kwargs):
        return json.loads(self.equipment.decode('utf-8'))

    def resolve_quests(self, info, **kwargs):
        return json.loads(self.quests.decode('utf-8'))


class MapAreaType(graphene.ObjectType):
    name = graphene.String()
    size_x = graphene.Int()
    size_y = graphene.Int()
    connections = graphene.List(graphene.String)


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
    characters = graphene.List(CharacterType)
    def resolve_characters(self, info, **kwargs):
        return Character.objects.filter(**kwargs)

    # TODO query single character

    # Skills
    skills = graphene.List(SkillType)
    def resolve_skills(self, info, **kwargs):
        return skill_list.values()

    # Map areas
    map_areas = graphene.List(MapAreaType)
    def resolve_map_areas(self, info, **kwargs):
        return areas.values()


##########################
# Mutation
##########################
class SendChatMessage(graphene.Mutation, name="SendChatMessagePayload"):  # type: ignore
    """Send chat message."""

    ok = graphene.Boolean()

    class Arguments:
        """Mutation arguments."""

        chatroom = graphene.String()
        text = graphene.String()

    def mutate(self, info, chatroom, text, **kwargs):
        """Mutation "resolver" - store and broadcast a message."""

        sender = kwargs.get('user')

        # Store a message.
        chats[chatroom].append({"chatroom": chatroom, "text": text, "sender": sender})

        # Notify subscribers.
        OnNewChatMessage.new_chat_message(chatroom=chatroom, text=text, sender=sender)

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
        base_skills = {'base_attack': skill_list['base_attack']}
        character.skills = json.dumps(base_skills).encode('utf-8')

        # Set item bag
        character.items = json.dumps({}).encode('utf-8')

        # Set equipments
        equipment = {
            'head': None,
            'torso': None,
            'legs': None,
            'weapon': None,
            'shield': None,
            'accessory_1': None,
            'accessory_2': None
        }
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
        x = location.get('x', 48)
        y = location.get('y', 48)
        character_id = kwargs.get('id')

        char = Character.objects.get(
            # user=kwargs.get('user'),
            id=character_id
        )
        if not target_position_is_valid([x, y], char.area_location):
            raise Exception('Invalid location')
        char.position_x = x
        char.position_y = y
        char.save()


        # TODO broadcast movement
        # OnCharacterMovement.character_movement(reference=reference, x=x, y=y)

        return UpdatePosition(char)


class CharacterLogIn(graphene.relay.ClientIDMutation):
    """Enters the game with a selected character"""
    
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
        char.is_logged = True
        char.save()

        # TODO Broadcast character login
        # OnCharacterLogIn.character_login(
        #     reference=char.name,
        #     x=position['x'],
        #     y=position['y']
        # )

        # API response

        return CharacterLogIn(True)


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

        # TODO Broadcast character login
        # OnCharacterLogIn.character_login(
        #     reference=char.name,
        #     x=position['x'],
        #     y=position['y']
        # )

        # API response

        return CharacterLogIn(True)


class Mutation:
    send_chat_message = SendChatMessage.Field()
    create_character = CreateCharacter.Field()
    update_position = UpdatePosition.Field()
    character_login = CharacterLogIn.Field()
    character_logout = CharacterLogOut.Field()


#################
# SUBSCRIPTIONS
#################


class OnNewChatMessage(channels_graphql_ws.Subscription):
    """Subscription triggers on a new chat message."""

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
            chatroom=chatroom, text=new_msg_text, sender=new_msg_sender
        )

    @classmethod
    def new_chat_message(cls, chatroom, text, sender):
        """Auxiliary function to send subscription notifications.
        It is generally a good idea to encapsulate broadcast invocation
        inside auxiliary class methods inside the subscription class.
        That allows to consider a structure of the `payload` as an
        implementation details.
        """
        cls.broadcast(
            group=chatroom,
            payload={"chatroom": chatroom, "text": text, "sender": sender},
        )


class Subscription(graphene.ObjectType):
    """GraphQL subscriptions."""

    on_new_chat_message = OnNewChatMessage.Field()
