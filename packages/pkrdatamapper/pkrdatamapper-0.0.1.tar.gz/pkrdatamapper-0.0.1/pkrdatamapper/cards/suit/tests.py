from django.test import TestCase
from ..suit.models import DBSuit
from pkrcomponents.components.cards.suit import Suit


class TestDBSuit(TestCase):

    def test_objects_from_list_returns_all_suits_when_db_is_populated(self):
        DBSuit.objects_from_list()
        assert DBSuit.objects.count() == len(list(Suit))

    def test_objects_from_list_creates_and_returns_suits_when_db_is_empty(self):
        DBSuit.objects.all().delete()
        suits = DBSuit.objects_from_list()
        assert len(suits) == len(list(Suit))
        assert DBSuit.objects.count() == len(list(Suit))

    def test_objects_from_list_returns_correct_suits(self, suit):
        DBSuit.objects.all().delete()
        suits = DBSuit.objects_from_list()
        assert suit.name in [db_suit.name for db_suit in suits]

    def test_from_suit_creates_new_entry_if_not_exists(self):
        DBSuit.objects.all().delete()
        suit = list(Suit)[0]
        db_suit = DBSuit.from_suit(suit)
        assert DBSuit.objects.count() == 1
        assert db_suit.name == suit.name

    def test_from_suit_returns_existing_entry_if_exists(self):
        suit = list(Suit)[0]
        DBSuit.from_suit(suit)
        db_suit = DBSuit.from_suit(suit)
        assert DBSuit.objects.count() == 1
        assert db_suit.name == suit.name