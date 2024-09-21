from django.core.management.base import BaseCommand
from django.db import connection



from pkrdatamapper.histories.player_hand_stats.models import DBPlayerHandStats
from pkrdatamapper.histories.street_player_hand_stats.general import DBGeneralHandStats
from pkrdatamapper.histories.street_player_hand_stats.preflop import DBPreflopHandStats
from pkrdatamapper.histories.street_player_hand_stats.postflop_stats.flop import DBFlopHandStats
from pkrdatamapper.histories.street_player_hand_stats.postflop_stats.river import DBRiverHandStats
from pkrdatamapper.histories.street_player_hand_stats.postflop_stats.turn import DBTurnHandStats
from pkrdatamapper.histories.hand_history.models import DBHandHistory


class Command(BaseCommand):
    help = ("Purge all objects from the following models: DBGeneralHandStats, DBPreflopHandStats, DBFlopHandStats, "
            "DBTurnHandStats, DBRiverHandStats, DBPlayerHandStats")

    def handle(self, *args, **kwargs):
        self.purge_duplicates()

    def purge_duplicates(self):
        models_to_purge = [DBGeneralHandStats, DBPreflopHandStats, DBFlopHandStats, DBTurnHandStats, DBRiverHandStats,
                           DBPlayerHandStats, DBHandHistory]
        print("Purging all objects from the following models:")
        for model in models_to_purge:
            table_name = model._meta.db_table
            print(f"Reinitializing table {table_name}")
            self.reinit_table(table_name)

    @staticmethod
    def reinit_table(table_name):
        with connection.cursor() as cursor:
            cursor.execute(f"TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE")
            print(f"Table {table_name} has been reinitialized")


