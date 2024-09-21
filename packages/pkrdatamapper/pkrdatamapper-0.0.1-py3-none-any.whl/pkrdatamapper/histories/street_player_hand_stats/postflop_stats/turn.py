from pkrdatamapper.histories.street_player_hand_stats.postflop_stats.base import DBPostflopPlayerHandStats


class DBTurnHandStats(DBPostflopPlayerHandStats):
    """A Database class to store turn player stats, resulting from the analysis of hand histories."""
    prefix = 'turn'

    class Meta:
        verbose_name = 'Turn Player Hand Stats'
        db_table = 'turn_player_hand_stats'
