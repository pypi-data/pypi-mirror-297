from django.db.models import ForeignKey, CASCADE, Model, OneToOneField

from pkrcomponents.components.players.table_player import TablePlayer

from pkrdatamapper.common.mixins import DFDataMixin
from pkrdatamapper.players.player.models import DBPlayer
from pkrdatamapper.histories.hand_history.models import DBHandHistory
from pkrdatamapper.histories.street_player_hand_stats.general import DBGeneralHandStats
from pkrdatamapper.histories.street_player_hand_stats.preflop import DBPreflopHandStats
from pkrdatamapper.histories.street_player_hand_stats.postflop_stats.river import DBRiverHandStats
from pkrdatamapper.histories.street_player_hand_stats.postflop_stats.turn import DBTurnHandStats
from pkrdatamapper.histories.street_player_hand_stats.postflop_stats.flop import DBFlopHandStats


class DBPlayerHandStats(Model, DFDataMixin):
    """
    A Database class to store player stats, resulting from the analysis of hand histories.
    """
    hand_history = ForeignKey(DBHandHistory,  on_delete=CASCADE)
    player = ForeignKey(DBPlayer, on_delete=CASCADE)
    general_stats = OneToOneField(DBGeneralHandStats, on_delete=CASCADE, related_name='general_stats', null=True)
    preflop_stats = OneToOneField(DBPreflopHandStats, on_delete=CASCADE, related_name='preflop_stats', null=True)
    flop_stats = OneToOneField(DBFlopHandStats, on_delete=CASCADE, related_name='flop_stats', null=True)
    turn_stats = OneToOneField(DBTurnHandStats, on_delete=CASCADE, related_name='turn_stats', null=True)
    river_stats = OneToOneField(DBRiverHandStats, on_delete=CASCADE, related_name='river_stats', null=True)

    @classmethod
    def from_table_player(cls, table_player: TablePlayer):
        db_player = DBPlayer.from_table_player(table_player)
        hand_history = DBHandHistory.from_table(table_player.table)
        db_player_hand_stats, _ = cls.objects.update_or_create(
            player=db_player,
            hand_history=hand_history,
            defaults={
                'general_stats': DBGeneralHandStats.from_stats(player=db_player, hand_history=hand_history,
                                                               general_stats=table_player.hand_stats.general),
                'preflop_stats': DBPreflopHandStats.from_stats(player=db_player, hand_history=hand_history,
                                                               preflop_stats=table_player.hand_stats.preflop),
                'flop_stats': DBFlopHandStats.from_stats(player=db_player, hand_history=hand_history,
                                                         postflop_stats=table_player.hand_stats.flop),
                'turn_stats': DBTurnHandStats.from_stats(player=db_player, hand_history=hand_history,
                                                         postflop_stats=table_player.hand_stats.turn),
                'river_stats': DBRiverHandStats.from_stats(player=db_player, hand_history=hand_history,
                                                           postflop_stats=table_player.hand_stats.river)
            }
        )
        return db_player_hand_stats

    class Meta:
        unique_together = ('hand_history', 'player')
        db_table = 'player_hand_stats'
        verbose_name = "Player Hand Stats"
        verbose_name_plural = "Player Hand Stats"
        ordering = ['hand_history', 'player']
