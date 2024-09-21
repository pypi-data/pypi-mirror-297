from pkrdatamapper.histories.street_player_hand_stats.postflop_stats.base import DBPostflopPlayerHandStats


class DBFlopHandStats(DBPostflopPlayerHandStats):
    """A Database class to store flop player stats, resulting from the analysis of hand histories."""
    prefix = 'flop'

    class Meta:
        verbose_name = 'Flop Player Hand Stats'
        db_table = 'flop_player_hand_stats'
