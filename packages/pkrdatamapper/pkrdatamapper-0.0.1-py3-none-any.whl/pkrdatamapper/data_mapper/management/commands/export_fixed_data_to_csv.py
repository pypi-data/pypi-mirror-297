from django.core.management.base import BaseCommand
from pkrdatamapper.actions.models import DBActionMove, DBActionsSequence, DBBlindType, DBStreet
from pkrdatamapper.cards.models import DBCard, DBCombo, DBFlop, DBHand, DBRank, DBShape, DBSuit
from pkrdatamapper.players.models import DBPosition, DBPositionsMap
from pkrdatamapper.tournaments.models import DBTourSpeed, DBTourType


class Command(BaseCommand):
    help = "Export data to CSV files for fixed data models"

    def handle(self, *args, **kwargs):
        print("Exporting data to CSV files")
        print("This may take a while...")
        models_to_export = [
            DBActionMove,
            DBActionsSequence,
            DBBlindType,
            DBStreet,
            DBCard,
            DBCombo,
            DBFlop,
            DBHand,
            DBRank,
            DBShape,
            DBSuit,
            DBPosition,
            DBPositionsMap,
            DBTourSpeed,
            DBTourType
        ]
        for model in models_to_export:
            model.export_to_csv()
        print("Data exported successfully!")
