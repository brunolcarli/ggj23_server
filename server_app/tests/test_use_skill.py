import json
from django.test import TestCase
from server_app.models import Character
from server_app.engine import use_skill
from django.contrib.auth.models import User
from server_app.skills import skill_list

class TestUseSkill(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='TestUser1', email='test@user.1', password='12345')
        self.user2 = User.objects.create(username='TestUser2', email='test@user.2', password='12345')
        self.attacker = Character.objects.create(name='TestChar1', class_type='dps', user=self.user1)
        self.defender = Character.objects.create(name='TestChar2', class_type='tanker', user=self.user2)
        self.attacker.skills = json.dumps(skill_list).encode('utf-8')

    def test_target_is_reachable_with_range_1(self):
        """
        Validate that skill reaches all coordinates the skill range allows.
        Test for skill range 1
        Simulate in a map with size 480x480
        """
        # Set attacker to stay on position x(4), y(50) in a grid of ten 48px blocks
        self.attacker.position_x = 192
        self.attacker.position_y = 240

        # Set defender to be on the right block after the attacker
        self.defender.position_x = self.attacker.position_x + 48
        self.defender.position_y = self.attacker.position_y

        self.assertTrue(use_skill(self.attacker, 'base_attack', self.defender))

        # Set defender to be on the left block after the attacker
        self.defender.position_x = self.attacker.position_x - 48
        self.defender.position_y = self.attacker.position_y

        self.assertTrue(use_skill(self.attacker, 'base_attack', self.defender))

        # Set defender to be one block undr the attacker
        self.defender.position_x = self.attacker.position_x
        self.defender.position_y = self.attacker.position_y + 48

        self.assertTrue(use_skill(self.attacker, 'base_attack', self.defender))

        # Set defender to be one block above the attacker
        self.defender.position_x = self.attacker.position_x
        self.defender.position_y = self.attacker.position_y - 48

        self.assertTrue(use_skill(self.attacker, 'base_attack', self.defender))

    def test_target_is_unreachable_with_range_1(self):
        """
        Validate that skill used cannot reach the selected target.
        Simulate in a map with size 480x480
        """
        # Set attacker to stay on position x(4), y(50) in a grid of ten 48px blocks
        self.attacker.position_x = 192
        self.attacker.position_y = 240

        # Set defender to be two blocks after the attacker right side
        self.defender.position_x = self.attacker.position_x + 96
        self.defender.position_y = self.attacker.position_y

        self.assertRaises(Exception, use_skill(self.attacker, 'base_attack', self.defender))

        # Set defender to be two blocks before the attacker left side
        self.defender.position_x = self.attacker.position_x - 96
        self.defender.position_y = self.attacker.position_y

        self.assertRaises(Exception, use_skill(self.attacker, 'base_attack', self.defender))

        # Set defender to be two blocks under the attacker
        self.defender.position_x = self.attacker.position_x
        self.defender.position_y = self.attacker.position_y + 96

        self.assertRaises(Exception, use_skill(self.attacker, 'base_attack', self.defender))

        # Set defender to be two blocks above the attacker
        self.defender.position_x = self.attacker.position_x
        self.defender.position_y = self.attacker.position_y - 96

        self.assertRaises(Exception, use_skill(self.attacker, 'base_attack', self.defender))

    def test_target_is_reachable_with_range_3(self):
        """
        Validate that skill reaches all coordinates the skill range allows.
        Test with skill range 3
        Simulate in a map with size 480x480
        """
        # Set attacker to stay on position x(4), y(50) in a grid of ten 48px blocks
        self.attacker.position_x = 192
        self.attacker.position_y = 240

        # Set defender to be on the right block after the attacker
        self.defender.position_x = self.attacker.position_x + (48*3)
        self.defender.position_y = self.attacker.position_y

        self.assertTrue(use_skill(self.attacker, 'fireball', self.defender))

        # Set defender to be on the left block after the attacker
        self.defender.position_x = self.attacker.position_x - (48*3)
        self.defender.position_y = self.attacker.position_y

        self.assertTrue(use_skill(self.attacker, 'fireball', self.defender))

        # Set defender to be one block undr the attacker
        self.defender.position_x = self.attacker.position_x
        self.defender.position_y = self.attacker.position_y + (48*3)

        self.assertTrue(use_skill(self.attacker, 'fireball', self.defender))

        # Set defender to be one block above the attacker
        self.defender.position_x = self.attacker.position_x
        self.defender.position_y = self.attacker.position_y - (48*3)

        self.assertTrue(use_skill(self.attacker, 'fireball', self.defender))

    def test_target_is_unreachable_with_range_3(self):
        """
        Validate that skill used cannot reach the selected target.
        Test with skill range 3
        Simulate in a map with size 480x480
        """
        # Set attacker to stay on position x(4), y(50) in a grid of ten 48px blocks
        self.attacker.position_x = 192
        self.attacker.position_y = 240

        # Set defender to be two blocks after the attacker right side
        self.defender.position_x = self.attacker.position_x + (48*5)
        self.defender.position_y = self.attacker.position_y

        self.assertRaises(Exception, use_skill(self.attacker, 'fireball', self.defender))

        # Set defender to be two blocks before the attacker left side
        self.defender.position_x = self.attacker.position_x - (48*5)
        self.defender.position_y = self.attacker.position_y

        self.assertRaises(Exception, use_skill(self.attacker, 'fireball', self.defender))

        # Set defender to be two blocks under the attacker
        self.defender.position_x = self.attacker.position_x
        self.defender.position_y = self.attacker.position_y + (48*5)

        self.assertRaises(Exception, use_skill(self.attacker, 'fireball', self.defender))

        # Set defender to be two blocks above the attacker
        self.defender.position_x = self.attacker.position_x
        self.defender.position_y = self.attacker.position_y - (48*5)

        self.assertRaises(Exception, use_skill(self.attacker, 'fireball', self.defender))

    def test_target_is_reachable_at_diagonal(self):
        """
        Validate that skill reaches all coordinates the skill range allows in diagonals.
        Test for skill range 1
        Simulate in a map with size 480x480
        """
        # Set attacker to stay on position x(4), y(50) in a grid of ten 48px blocks
        self.attacker.position_x = 192
        self.attacker.position_y = 240

        self.defender.position_x = self.attacker.position_x + 48
        self.defender.position_y = self.attacker.position_y + 48

        self.assertTrue(use_skill(self.attacker, 'base_attack', self.defender))

        self.defender.position_x = self.attacker.position_x + 48
        self.defender.position_y = self.attacker.position_y - 48

        self.assertTrue(use_skill(self.attacker, 'base_attack', self.defender))

        # Set defender to be one block under the attacker
        self.defender.position_x = self.attacker.position_x - 48
        self.defender.position_y = self.attacker.position_y - 48

        self.assertTrue(use_skill(self.attacker, 'base_attack', self.defender))

        # Set defender to be one block above the attacker
        self.defender.position_x = self.attacker.position_x - 48
        self.defender.position_y = self.attacker.position_y + 48

        self.assertTrue(use_skill(self.attacker, 'base_attack', self.defender))
