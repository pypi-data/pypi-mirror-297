from django.db import models

from pkrdatamapper.common.mixins import DFDataMixin
from pkrdatamapper.histories.street_player_hand_stats.base import DBStreetPlayerHandStats
from pkrdatamapper.players.models import DBPlayer
from pkrdatamapper.players.street_player_stats.meta import DBPlayerStatsMeta


class DBStreetPlayerStatsBase(models.base.ModelBase, DBPlayerStatsMeta):
    pass


class DBStreetPlayerStats(models.Model, DFDataMixin, metaclass=DBStreetPlayerStatsBase):
    """
    A Database class to store player stats, resulting from the analysis of hand histories.
    """
    associated_model: DBStreetPlayerHandStats
    player = models.OneToOneField(DBPlayer, on_delete=models.CASCADE)

    @classmethod
    def from_player_stats(cls, player_stats):
        street_stats, _ = cls.objects.update_or_create(player=player_stats.player)
        return street_stats

    class Meta:
        abstract = True
