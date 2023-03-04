import json

from django.db import models
from django.contrib.auth.models import User


class Character(models.Model):
    """
    Defines data structure for a playable character.
    """
    name = models.CharField(max_length=50, null=False, blank=False)
    lv = models.IntegerField(default=1)
    next_lv = models.IntegerField(default=1)
    exp = models.IntegerField(default=0)
    max_hp = models.IntegerField(default=200)
    max_sp = models.IntegerField(default=100)
    current_hp = models.IntegerField(default=200)
    current_sp = models.IntegerField(default=100)
    power = models.IntegerField(default=10)
    resistance = models.IntegerField(default=10)
    agility = models.IntegerField(default=1)
    is_ko = models.BooleanField(default=False)
    is_logged = models.BooleanField(default=False)
    last_activity = models.DateTimeField(null=True)
    position_x = models.IntegerField(default=20, null=False)
    position_y = models.IntegerField(default=20, null=False)
    area_location = models.CharField(max_length=55, null=False, blank=False, default='citadel_central_area')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    items = models.BinaryField(default=json.dumps(dict()).encode('utf-8'))
    equipment = models.BinaryField(null=True)
    skills = models.BinaryField(null=False)
    quests = models.BinaryField(null=True)
    class_type = models.CharField(max_length=25, null=False, blank=False)
    effects = models.BinaryField(null=True)
    aim = models.IntegerField(default=100)
    wallet = models.BigIntegerField(default=0)
    ep = models.IntegerField(default=0)  # Evolution Points
    respawn_spot = models.CharField(max_length=55, null=False, blank=False, default='citadel_central_area')
    equipped_skill = models.IntegerField(null=True)
    equipped_item = models.IntegerField(null=True)


    def getItems(self):
        return json.loads(self.items.decode('utf-8'))
    
    def setItems(self, items):
        self.items = json.dumps(items).encode('utf-8')


class ItemOffer(models.Model):
    """
    Defines item offer to be bought by other players
    """
    seller = models.ForeignKey(Character, on_delete=models.CASCADE, null=False)
    price = models.BigIntegerField(default=0)
    items = models.BinaryField(default=b'{}')
    
    def getItems(self):
        return json.loads(self.items.decode('utf-8'))
    
    def setItems(self, items):
        self.items = json.dumps(items).encode('utf-8')


class SpawnedEnemy(models.Model):
    lv = models.IntegerField(default=1)
    name = models.CharField(max_length=50, null=False, blank=False)
    exp = models.IntegerField(default=0)
    max_hp = models.IntegerField(default=200)
    max_sp = models.IntegerField(default=99999)
    current_hp = models.IntegerField(default=200)
    current_sp = models.IntegerField(default=99999)
    power = models.IntegerField(default=10)
    resistance = models.IntegerField(default=10)
    agility = models.IntegerField(default=1)
    is_ko = models.BooleanField(default=False)
    position_x = models.IntegerField(default=48, null=False)
    position_y = models.IntegerField(default=48, null=False)
    area_location = models.CharField(max_length=55, null=False, blank=False)
    aim = models.IntegerField(default=100)
    skills = models.BinaryField(null=False)
    class_type = models.CharField(max_length=25, null=False, blank=False, default='enemy')
    effects = models.BinaryField(null=True)
    drops = models.BinaryField(null=True)

