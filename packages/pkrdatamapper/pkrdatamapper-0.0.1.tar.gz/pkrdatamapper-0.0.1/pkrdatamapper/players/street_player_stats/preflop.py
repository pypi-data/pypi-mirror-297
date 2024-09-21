from pkrdatamapper.histories.street_player_hand_stats.preflop import DBPreflopHandStats
from pkrdatamapper.players.street_player_stats.base import DBStreetPlayerStats


class DBPreflopPlayerStats(DBStreetPlayerStats):
    associated_model = DBPreflopHandStats

    class Meta:
        verbose_name = 'Preflop Player Stats'
        db_table = 'preflop_player_stats'
