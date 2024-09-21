from django.core.management.base import BaseCommand
from pkrdatamapper.players.models import DBPlayerStats
from concurrent.futures import ThreadPoolExecutor, as_completed


class Command(BaseCommand):
    help = "Update the stats of all players"

    def handle(self, *args, **kwargs):
        self.update_stats()

    @staticmethod
    def update_stats():
        DBPlayerStats.update_all_stats()