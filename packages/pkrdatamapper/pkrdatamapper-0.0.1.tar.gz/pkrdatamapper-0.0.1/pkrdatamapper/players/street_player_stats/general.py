from pkrdatamapper.histories.street_player_hand_stats.general import DBGeneralHandStats
from pkrdatamapper.players.street_player_stats.base import DBStreetPlayerStats


class DBGeneralPlayerStats(DBStreetPlayerStats):
    associated_model = DBGeneralHandStats

    class Meta:
        verbose_name = 'General Player Stats'
        db_table = 'general_player_stats'

