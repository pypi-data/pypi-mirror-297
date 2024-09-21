from django.db import models
from pkrcomponents.components.players.position import Position
from pkrdatamapper.common.mixins import DFDataMixin


class DBPosition(models.Model, DFDataMixin):
    """Represents a position in poker"""

    name = models.CharField(max_length=10, unique=True)
    short_name = models.CharField(max_length=4, unique=True)
    symbol = models.CharField(max_length=4, unique=True)
    is_early = models.BooleanField(default=False)
    is_middle = models.BooleanField(default=False)
    is_late = models.BooleanField(default=False)
    is_blind = models.BooleanField(default=False)
    preflop_order = models.PositiveSmallIntegerField(unique=True)
    postflop_order = models.PositiveSmallIntegerField(unique=True)

    def __str__(self):
        return self.name

    @classmethod
    def from_position(cls, position: Position):
        db_position, _ = cls.objects.get_or_create(
            name=position.name,
            defaults={
                'short_name': position.short_name,
                'symbol': position.symbol,
                'is_early': position.is_early,
                'is_middle': position.is_middle,
                'is_late': position.is_late,
                'is_blind': position.is_blind,
                'preflop_order': position.preflop_order,
                'postflop_order': position.postflop_order
            }
        )
        return db_position

    @classmethod
    def objects_from_list(cls):
        if cls.objects.count() == len(Position):
            return cls.objects.all()
        return [cls.from_position(position) for position in list(Position)]

    class Meta:
        verbose_name = "Position"
        verbose_name_plural = "Positions"
        db_table = 'positions'
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_position')
        ]
