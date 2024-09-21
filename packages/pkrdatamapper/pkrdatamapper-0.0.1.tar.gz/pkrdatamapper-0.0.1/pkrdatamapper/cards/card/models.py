from django.db import models
from pkrcomponents.components.cards.card import Card
from pkrdatamapper.common.mixins import DFDataMixin
from pkrdatamapper.cards.suit.models import DBSuit
from pkrdatamapper.cards.rank.models import DBRank
from pkrdatamapper.data_mapper.utils.exceptions import NoCardError


class DBCard(models.Model, DFDataMixin):
    name = models.CharField(max_length=20, unique=True)
    short_name = models.CharField(max_length=2, unique=True)
    symbol = models.CharField(max_length=2, unique=True)
    is_broadway = models.BooleanField(default=False)
    is_face = models.BooleanField(default=False)
    suit = models.ForeignKey(DBSuit, on_delete=models.CASCADE)
    rank = models.ForeignKey(DBRank, on_delete=models.CASCADE)

    def __str__(self):
        return self.short_name

    @classmethod
    def from_card(cls, card: Card):
        if not card:
            return None
        suit = DBSuit.from_suit(card.suit)
        rank = DBRank.from_rank(card.rank)
        db_card, _ = cls.objects.get_or_create(
            short_name=card.short_name,
            defaults={
                'name': card.name,
                'symbol': card.symbol,
                'is_broadway': card.is_broadway,
                'is_face': card.is_face,
                'suit': suit,
                'rank': rank
            }
        )
        return db_card

    @classmethod
    def objects_from_list(cls):
        if cls.objects.count() == len(Card):
            return cls.objects.all()
        return [cls.from_card(card) for card in list(Card)]

    class Meta:
        app_label = "cards"
        verbose_name = "Card"
        verbose_name_plural = "Cards"
        constraints = [
            models.UniqueConstraint(fields=['rank', 'suit'], name='unique_card')
        ]
        db_table = 'cards'
