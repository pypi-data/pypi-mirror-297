import django
from django.apps import apps
if not apps.ready:
    django.setup()

from pkrdatamapper.players.position.models import DBPosition
from pkrdatamapper.players.positions_map.models import DBPositionsMap


def populate_db():
    db_classes = [DBPosition, DBPositionsMap]
    for db_class in db_classes:
        db_class.objects_from_list()


if __name__ == '__main__':
    populate_db()
