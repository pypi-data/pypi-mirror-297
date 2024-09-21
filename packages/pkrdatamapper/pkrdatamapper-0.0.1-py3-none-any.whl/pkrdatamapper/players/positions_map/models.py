from django.db import models
from pkrcomponents.components.players.positions_map import PositionsMap
from ..position.models import DBPosition
from pkrdatamapper.common.mixins import DFDataMixin


class DBPositionsMap(models.Model, DFDataMixin):
    cnt_players = models.PositiveSmallIntegerField()
    has_sb = models.BooleanField()
    has_bb = models.BooleanField()
    has_btn = models.BooleanField()
    positions = models.ManyToManyField(DBPosition)

    @classmethod
    def from_positions_map(cls, positions_map: PositionsMap):
        db_positions_map, _ = cls.objects.get_or_create(
            cnt_players=positions_map.cnt_players,
            has_sb=positions_map.has_sb,
            has_bb=positions_map.has_bb,
            has_btn=positions_map.has_btn)
        db_positions = [DBPosition.from_position(pos) for pos in positions_map.positions]
        db_positions_map.positions.set(db_positions)
        return db_positions_map

    @classmethod
    def objects_from_list(cls):

        if cls.objects.count() == len(PositionsMap):
            return cls.objects.all()
        return [cls.from_positions_map(positions_map) for positions_map in list(PositionsMap)]

    class Meta:
        verbose_name = "Positions Map"
        verbose_name_plural = "Positions Maps"
        db_table = 'positions_maps'
        constraints = [
            models.UniqueConstraint(fields=['cnt_players', 'has_sb', 'has_bb', 'has_btn'], name='unique_positions_map')
        ]
