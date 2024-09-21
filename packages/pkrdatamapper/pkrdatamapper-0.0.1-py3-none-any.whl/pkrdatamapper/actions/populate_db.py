import django
from django.apps import apps
if not apps.ready:
    django.setup()

from pkrdatamapper.actions.action_move.models import DBActionMove
from pkrdatamapper.actions.blind_type.models import DBBlindType
from pkrdatamapper.actions.street.models import DBStreet


def populate_db():
    db_classes = [DBActionMove, DBBlindType, DBStreet]
    for db_class in db_classes:
        db_class.objects_from_list()


if __name__ == '__main__':
    populate_db()
