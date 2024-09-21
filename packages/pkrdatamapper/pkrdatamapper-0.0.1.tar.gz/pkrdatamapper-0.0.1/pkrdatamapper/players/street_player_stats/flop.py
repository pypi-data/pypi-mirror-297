from pkrdatamapper.histories.street_player_hand_stats.postflop_stats.flop import DBFlopHandStats
from pkrdatamapper.players.street_player_stats.base import DBStreetPlayerStats


class DBFlopPlayerStats(DBStreetPlayerStats):
    associated_model = DBFlopHandStats

    class Meta:
        verbose_name = 'Flop Player Stats'
        db_table = 'flop_player_stats'