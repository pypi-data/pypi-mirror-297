from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError


class Command(BaseCommand):
    help = 'Test database connection'

    def handle(self, *args, **kwargs):
        self.test_db_connection()

    @staticmethod
    def test_db_connection():
        db_conn = connections['default']
        try:
            db_conn.cursor()
            print("Connexion à la base de données réussie!")
        except OperationalError as e:
            print(e)
            print("Impossible de se connecter à la base de données.")
        finally:
            db_conn.close()

