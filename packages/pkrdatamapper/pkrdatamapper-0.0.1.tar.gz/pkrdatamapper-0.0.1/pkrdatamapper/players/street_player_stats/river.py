from pkrdatamapper.histories.street_player_hand_stats.postflop_stats.river import DBRiverHandStats
from pkrdatamapper.players.street_player_stats.base import DBStreetPlayerStats


class DBRiverPlayerStats(DBStreetPlayerStats):
    associated_model = DBRiverHandStats

    class Meta:
        verbose_name = 'River Player Stats'
        db_table = 'river_player_stats'