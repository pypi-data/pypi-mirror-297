from django.db import models
from pkrdatamapper.common.fields import CountField
from pkrdatamapper.common.mixins import DFDataMixin

from pkrdatamapper.histories.player_hand_stats.models import DBPlayerHandStats
from pkrdatamapper.players.player.models import DBPlayer
from pkrdatamapper.players.street_player_stats.general import DBGeneralPlayerStats
from pkrdatamapper.players.street_player_stats.preflop import DBPreflopPlayerStats
from pkrdatamapper.players.street_player_stats.flop import DBFlopPlayerStats
from pkrdatamapper.players.street_player_stats.turn import DBTurnPlayerStats
from pkrdatamapper.players.street_player_stats.river import DBRiverPlayerStats


class DBPlayerStats(models.Model, DFDataMixin):
    """
    A Database class to store player stats, resulting from the analysis of hand histories.
    """
    player = models.ForeignKey(DBPlayer, on_delete=models.CASCADE)
    cnt_hands_played = CountField(associated_model=DBPlayerHandStats, default=0, db_comment='Number of hands played')
    general_stats = models.OneToOneField(DBGeneralPlayerStats, on_delete=models.CASCADE, null=True)
    preflop_stats = models.OneToOneField(DBPreflopPlayerStats, on_delete=models.CASCADE, null=True)
    flop_stats = models.OneToOneField(DBFlopPlayerStats, on_delete=models.CASCADE, null=True)
    turn_stats = models.OneToOneField(DBTurnPlayerStats, on_delete=models.CASCADE, null=True)
    river_stats = models.OneToOneField(DBRiverPlayerStats, on_delete=models.CASCADE, null=True)

    def update_stats(self):
        player_stats, _ = self.__class__.objects.update_or_create(
            player=self.player,
            defaults=dict(
                general_stats=DBGeneralPlayerStats.from_player_stats(self),
                preflop_stats=DBPreflopPlayerStats.from_player_stats(self),
                flop_stats=DBFlopPlayerStats.from_player_stats(self),
                turn_stats=DBTurnPlayerStats.from_player_stats(self),
                river_stats=DBRiverPlayerStats.from_player_stats(self)
            )

        )
        player_stats.save()

    @classmethod
    def update_all_stats(cls):
        print("Updating all players' stats...")
        players = cls.objects.all()
        for player in players:
            player.update_stats()
        print("All players' stats have been updated")


    class Meta:
        db_table = 'player_stats'
        unique_together = ('player',)
        ordering = ['player']

