from django.db import models
from pkrcomponents.components.tournaments.level import Level
from pkrdatamapper.common.mixins import DFDataMixin


class DBLevel(models.Model, DFDataMixin):
    value = models.PositiveSmallIntegerField()
    sb = models.FloatField()
    bb = models.FloatField()
    ante = models.FloatField()

    @classmethod
    def from_level(cls, level: Level):
        db_level, _ = cls.objects.get_or_create(
            value=level.value,
            sb=level.sb,
            bb=level.bb,
            ante=level.ante
        )
        return db_level

    class Meta:
        db_table = 'levels'
        verbose_name = "Level"
        verbose_name_plural = "Levels"
        constraints = [
            models.UniqueConstraint(fields=['value', 'sb', 'bb', 'ante'], name='unique_level')
        ]
