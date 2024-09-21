import django
from django.apps import apps


if not apps.ready:
    django.setup()
from pkrdatamapper.tournaments.speed.models import DBTourSpeed
from pkrdatamapper.tournaments.type.models import DBTourType



def populate_db():
    db_classes = [DBTourSpeed, DBTourType]
    for db_class in db_classes:
        db_class.objects_from_list()


if __name__ == '__main__':
    print("Populating the databases...")
    populate_db()
