from django.db import models
from django.contrib.auth import get_user_model


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
    last_activity = models.DateField(null=True)
    position_x = models.IntegerField(default=48, null=False)
    position_y = models.IntegerField(default=48, null=False)
    area_location = models.CharField(max_length=25, null=False, blank=False, default='citadel')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=False)
    items = models.BinaryField(null=True)
    equipment = models.BinaryField(null=True)
    skills = models.BinaryField(null=False)
    quests = models.BinaryField(null=True)
    class_type = models.CharField(max_length=25, null=False, blank=False)
