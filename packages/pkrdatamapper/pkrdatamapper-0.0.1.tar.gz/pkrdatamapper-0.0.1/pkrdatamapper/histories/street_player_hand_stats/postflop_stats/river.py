from pkrdatamapper.histories.street_player_hand_stats.postflop_stats.base import DBPostflopPlayerHandStats


class DBRiverHandStats(DBPostflopPlayerHandStats):
    """A Database class to store river player stats, resulting from the analysis of hand histories."""
    prefix = 'river'

    class Meta:
        verbose_name = 'River Player Hand Stats'
        db_table = 'river_player_hand_stats'
