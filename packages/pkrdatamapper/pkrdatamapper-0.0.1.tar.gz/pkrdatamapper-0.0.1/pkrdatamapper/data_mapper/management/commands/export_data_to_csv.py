from django.core.management.base import BaseCommand
from pkrdatamapper.histories.hand_history.models import DBHandHistory
from pkrdatamapper.histories.player_hand_stats import models as player_hand_stats_models
from pkrdatamapper.players.models import DBPlayerStats, DBPlayer
from pkrdatamapper.tournaments.models import DBBuyIn, DBLevel, DBRefTournament, DBTournament


class Command(BaseCommand):
    help = "Export data to CSV files"

    def handle(self, *args, **kwargs):
        print("Exporting data to CSV files")
        print("This may take a while...")
        models_to_export = [
            DBTournament,
            DBRefTournament,
            DBBuyIn,
            DBLevel,
            DBPlayer,
            DBHandHistory,
            DBPlayerStats,
            player_hand_stats_models.DBPlayerHandStats,
            player_hand_stats_models.DBGeneralHandStats,
            player_hand_stats_models.DBPreflopHandStats,
            player_hand_stats_models.DBFlopHandStats,
            player_hand_stats_models.DBTurnHandStats,
            player_hand_stats_models.DBRiverHandStats
        ]
        for model in models_to_export:
            model.export_to_csv()
        print("Data exported successfully!")

