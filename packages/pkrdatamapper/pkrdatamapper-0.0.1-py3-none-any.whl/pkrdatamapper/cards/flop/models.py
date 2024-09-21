from django.db import models
from pkrcomponents.components.cards.flop import Flop
from pkrdatamapper.data_mapper.utils.exceptions import NoFlopError, NoCardError
from pkrdatamapper.cards.card.models import DBCard
from pkrdatamapper.common.mixins import DFDataMixin


class DBFlop(models.Model, DFDataMixin):
    short_name = models.CharField(max_length=6, unique=True)
    symbol = models.CharField(max_length=6, unique=True)
    first_card = models.ForeignKey(DBCard, related_name='first_flop_card', on_delete=models.CASCADE)
    second_card = models.ForeignKey(DBCard, related_name='second_flop_card', on_delete=models.CASCADE)
    third_card = models.ForeignKey(DBCard, related_name='third_flop_card', on_delete=models.CASCADE)
    is_rainbow = models.BooleanField(default=False)
    has_flush_draw = models.BooleanField(default=False)
    is_monotone = models.BooleanField(default=False)
    is_triplet = models.BooleanField(default=False)
    is_paired = models.BooleanField(default=False)
    is_sequential = models.BooleanField(default=False)
    has_straights = models.BooleanField(default=False)
    has_straight_draw = models.BooleanField(default=False)
    has_gutshot = models.BooleanField(default=False)
    min_distance = models.IntegerField(default=0)
    max_distance = models.IntegerField(default=0)

    def __str__(self):
        return self.short_name

    @classmethod
    def from_flop(cls, flop: Flop):
        """
        Create a DBFlop object from a Flop object. If there is no such object in the database, create it.
        In case no flop is given, return None.
        """
        try:
            first_card = DBCard.from_card(flop.first_card)
            second_card = DBCard.from_card(flop.second_card)
            third_card = DBCard.from_card(flop.third_card)
            db_flop, _ = cls.objects.get_or_create(
                short_name=flop.short_name,
                defaults={
                    'symbol': flop.symbol,
                    'first_card': first_card,
                    'second_card': second_card,
                    'third_card': third_card,
                    'is_rainbow': flop.is_rainbow,
                    'has_flush_draw': flop.has_flush_draw,
                    'is_monotone': flop.is_monotone,
                    'is_triplet': flop.is_triplet,
                    'is_paired': flop.is_paired,
                    'is_sequential': flop.is_sequential,
                    'has_straights': flop.has_straights,
                    'has_straight_draw': flop.has_straight_draw,
                    'has_gutshot': flop.has_gutshot,
                    'min_distance': flop.min_distance,
                    'max_distance': flop.max_distance
                }
            )
            return db_flop
        except AttributeError:
            return None

    @classmethod
    def objects_from_list(cls):
        if cls.objects.count() == len(Flop):
            return cls.objects.all()
        return [cls.from_flop(flop) for flop in list(Flop)]

    class Meta:
        verbose_name = "Flop"
        verbose_name_plural = "Flops"
        db_table = 'flops'
        constraints = [
            models.UniqueConstraint(fields=['short_name'], name='unique_flop')
        ]
