import django
from django.apps import apps
if not apps.ready:
    django.setup()

from pkrdatamapper.cards.card.models import DBCard
from pkrdatamapper.cards.combo.models import DBCombo

from pkrdatamapper.cards.suit.models import DBSuit
from pkrdatamapper.cards.rank.models import DBRank
from pkrdatamapper.cards.shape.models import DBShape
from pkrdatamapper.cards.hand.models import DBHand
from pkrdatamapper.cards.flop.models import DBFlop


def populate_db():
    db_classes = [DBSuit, DBRank, DBCard, DBShape, DBHand, DBCombo, DBFlop]
    for db_class in db_classes:
        db_class.objects_from_list()


if __name__ == '__main__':
    populate_db()
