import django
from django.apps import apps
from django.core.management.base import BaseCommand

if not apps.ready:
    django.setup()

from pkrdatamapper.actions import populate_db as actions_populate_db
from pkrdatamapper.cards import populate_db as cards_populate_db
from pkrdatamapper.players import populate_db as players_populate_db
from pkrdatamapper.tournaments import populate_db as tournaments_populate_db


class Command(BaseCommand):
    help = 'Test database connection'

    def handle(self, *args, **kwargs):
        self.populate_db()

    @staticmethod
    def populate_db():
        print("Populating database")
        print("This may take a while...")
        print("Populating actions...\n")
        actions_populate_db.populate_db()
        print("Populating cards...\n")
        cards_populate_db.populate_db()
        print("Populating players...\n")
        players_populate_db.populate_db()
        print("Populating tournaments...\n")
        tournaments_populate_db.populate_db()

