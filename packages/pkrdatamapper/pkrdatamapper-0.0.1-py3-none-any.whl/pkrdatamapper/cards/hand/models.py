from django.db import models
from pkrcomponents.components.cards.hand import Hand
from ..rank.models import DBRank
from ..shape.models import DBShape
from pkrdatamapper.common.mixins import DFDataMixin


class DBHand(models.Model, DFDataMixin):
    short_name = models.CharField(max_length=3, unique=True)
    first_rank = models.ForeignKey(DBRank, related_name='first_rank', on_delete=models.CASCADE)
    second_rank = models.ForeignKey(DBRank, related_name='second_rank', on_delete=models.CASCADE)
    shape = models.ForeignKey(DBShape, on_delete=models.CASCADE)
    is_suited = models.BooleanField(default=False)
    is_offsuit = models.BooleanField(default=True)
    is_paired = models.BooleanField(default=False)
    is_connector = models.BooleanField(default=False)
    is_one_gapper = models.BooleanField(default=False)
    is_two_gapper = models.BooleanField(default=False)
    is_broadway = models.BooleanField(default=False)
    is_face = models.BooleanField(default=False)
    is_suited_connector = models.BooleanField(default=False)
    rank_difference = models.IntegerField(default=0)

    def __str__(self):
        return self.short_name

    @classmethod
    def from_hand(cls, hand: Hand):
        first_rank = DBRank.objects.get(name=hand.first.name)
        second_rank = DBRank.objects.get(name=hand.second.name)
        # shape = DBShape.objects.get(name=hand.shape.name)
        shape = DBShape.from_shape(hand.shape)
        db_hand, _ = cls.objects.get_or_create(
            short_name=f"{hand}",
            defaults={
                'first_rank': first_rank,
                'second_rank': second_rank,
                'shape': shape,
                'is_suited': hand.is_suited,
                'is_offsuit': hand.is_offsuit,
                'is_paired': hand.is_pair,
                'is_connector': hand.is_connector,
                'is_one_gapper': hand.is_one_gapper,
                'is_two_gapper': hand.is_two_gapper,
                'is_broadway': hand.is_broadway,
                'is_face': hand.is_face,
                'is_suited_connector': hand.is_suited_connector,
                'rank_difference': hand.rank_difference
            }
        )
        return db_hand

    @classmethod
    def objects_from_list(cls):
        if cls.objects.count() == len(Hand):
            return cls.objects.all()
        return [cls.from_hand(hand) for hand in list(Hand)]

    class Meta:
        verbose_name = "Hand"
        verbose_name_plural = "Hands"
        db_table = 'hands'
        constraints = [
            models.UniqueConstraint(fields=['short_name'], name='unique_hand')
        ]
