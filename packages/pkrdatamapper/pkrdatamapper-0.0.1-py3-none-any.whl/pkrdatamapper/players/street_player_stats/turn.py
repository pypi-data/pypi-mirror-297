from pkrdatamapper.histories.street_player_hand_stats.postflop_stats.turn import DBTurnHandStats
from pkrdatamapper.players.street_player_stats.base import DBStreetPlayerStats


class DBTurnPlayerStats(DBStreetPlayerStats):
    associated_model = DBTurnHandStats

    class Meta:
        verbose_name = 'Turn Player Stats'
        db_table = 'turn_player_stats'