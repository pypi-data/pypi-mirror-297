
from django.db import models

from pkrdatamapper.common.mixins import DFDataMixin

from pkrdatamapper.histories.hand_history.models import DBHandHistory
from pkrdatamapper.histories.street_player_hand_stats.meta import DBHandStatsMeta
from pkrdatamapper.players.player.models import DBPlayer


class StreetHandStatsBase(models.base.ModelBase, DBHandStatsMeta):
    pass


class DBStreetPlayerHandStats(models.Model, DFDataMixin, metaclass=StreetHandStatsBase):
    """
    A Database class to store postflop player stats, resulting from the analysis of hand histories.
    """
    data_fields: list
    data_attr_fields: list
    prefix: str

    player = models.ForeignKey(DBPlayer, on_delete=models.CASCADE)
    hand_history = models.ForeignKey(DBHandHistory, on_delete=models.CASCADE)

    class Meta:
        abstract = True
