from django.db import models
from pkrcomponents.components.cards.combo import Combo
from pkrdatamapper.common.mixins import DFDataMixin
from pkrdatamapper.cards.card.models import DBCard
from pkrdatamapper.cards.hand.models import DBHand


class DBCombo(models.Model, DFDataMixin):
    short_name = models.CharField(max_length=4, unique=True)
    symbol = models.CharField(max_length=4, unique=True)
    first_card = models.ForeignKey(DBCard, related_name='first_card', on_delete=models.CASCADE)
    second_card = models.ForeignKey(DBCard, related_name='second_card', on_delete=models.CASCADE)
    hand = models.ForeignKey(DBHand, on_delete=models.CASCADE)

    def __str__(self):
        return self.short_name

    @classmethod
    def from_combo(cls, combo: Combo):
        if not combo:
            return None
        first_card = DBCard.from_card(combo.first)
        second_card = DBCard.from_card(combo.second)
        hand = DBHand.from_hand(combo.hand)
        db_combo, _ = cls.objects.get_or_create(
            short_name=f"{combo.first.short_name}{combo.second.short_name}",
            defaults={
                'symbol': f"{combo.first.symbol}{combo.second.symbol}",
                'first_card': first_card,
                'second_card': second_card,
                'hand': hand,
            }
        )
        return db_combo

    @classmethod
    def objects_from_list(cls):
        if cls.objects.count() == len(Combo):
            return cls.objects.all()
        return [cls.from_combo(combo) for combo in list(Combo)]

    class Meta:
        verbose_name = "Combo"
        verbose_name_plural = "Combos"
        db_table = 'combos'
        constraints = [
            models.UniqueConstraint(fields=['short_name'], name='unique_combo')
        ]