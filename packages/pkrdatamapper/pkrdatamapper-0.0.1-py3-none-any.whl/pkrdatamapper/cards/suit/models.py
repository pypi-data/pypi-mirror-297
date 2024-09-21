from django.db import models
from pkrcomponents.components.cards.suit import Suit
from pkrdatamapper.common.mixins import DFDataMixin


class DBSuit(models.Model, DFDataMixin):
    name = models.CharField(max_length=8, unique=True)
    symbol = models.CharField(max_length=1, unique=True)
    short_name = models.CharField(max_length=1, unique=True)

    def __str__(self):
        return f"{self.short_name}"

    @classmethod
    def from_suit(cls, suit: Suit):
        db_suit, _ = cls.objects.get_or_create(
            name=suit.name,
            defaults = {
                'name': suit.name,
                'symbol': suit.symbol,
                'short_name': suit.short_name
            }
        )
        db_suit.save()
        return db_suit

    @classmethod
    def objects_from_list(cls):
        """
        Returns a list of all suits in the game
        If the suits are already in the database, it returns them
        If not, it creates them and returns them
        """
        if cls.objects.count() == len(Suit):
            return cls.objects.all()
        return [cls.from_suit(suit) for suit in list(Suit)]

    class Meta:
        verbose_name = "Suit"
        verbose_name_plural = "Suits"
        db_table = 'suits'
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_suit')
        ]
