from django.test import TestCase
from users.models import User, GameParticipation
from games.models import Game, Round, Zone

class TestModels(TestCase):

    def setUp(self):
        self.Zone = Zone( capacity=5)
        self.User = User(id=5)

    def test_user_is_assigned_attributes_on_creation(self):
        self.assertIs(self.User.__class__, User)
        self.assertEquals(self.User.is_gamekeeper, False)
        self.assertEquals(self.User.id, 5)

    def test_gameparticipation_is_assigned_attributes_on_creation(self):
        self.assertIs(self.GameParticipation.__class__, GameParticipation)
        self.assertEquals(self.GameParticipation.is_gamekeeper, False)
        self.assertEquals(selfGameParticipationr.id, 5)

    def test_zone_is_assigned_attributes_on_creation(self):
        self.assertIs(self.Zone.__class__, Zone)
        self.assertEquals(self.Zone.capacity, 5)

    def test_round_is_assigned_attributes_on_creation(self):
        self.assertIs(self.Round.__class__, Round)
        self.assertEquals(self.Round.capacity, 5)