from django.db import models
from pkrcomponents.components.cards.rank import Rank
from pkrdatamapper.common.mixins import DFDataMixin


class DBRank(models.Model, DFDataMixin):
    name = models.CharField(max_length=6, unique=True)
    symbol = models.CharField(max_length=1, unique=True)
    short_name = models.CharField(max_length=1, unique=True)
    is_broadway = models.BooleanField(default=False)
    is_face = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.short_name}"

    @classmethod
    def from_rank(cls, rank: Rank):
        db_rank, _ = cls.objects.get_or_create(
            name=rank.name,
            defaults={
                'symbol': rank.symbol,
                'short_name': rank.short_name,
                'is_broadway': rank.is_broadway,
                'is_face': rank.is_face
            }
        )
        db_rank.save()
        return db_rank

    @classmethod
    def objects_from_list(cls):
        if cls.objects.count() == len(Rank):
            return cls.objects.all()
        return [cls.from_rank(rank) for rank in list(Rank)]

    class Meta:
        verbose_name = "Rank"
        verbose_name_plural = "Ranks"
        db_table = 'ranks'
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_rank')
        ]
