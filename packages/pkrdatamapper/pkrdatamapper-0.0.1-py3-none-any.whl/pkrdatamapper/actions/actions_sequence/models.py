from django.db import models
from pkrcomponents.components.actions.actions_sequence import ActionsSequence
from pkrdatamapper.common.mixins import DFDataMixin


class DBActionsSequence(models.Model, DFDataMixin):
    symbol = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.symbol

    @classmethod
    def from_actions_sequence(cls, actions_sequence: ActionsSequence):
        if not actions_sequence:
            return None
        db_actions_sequence, _ = cls.objects.get_or_create(symbol=actions_sequence.symbol)
        return db_actions_sequence

    class Meta:
        verbose_name = "Actions Sequence"
        verbose_name_plural = "Actions Sequences"
        db_table = 'actions_sequences'
        constraints = [
            models.UniqueConstraint(fields=['symbol'], name='unique_actions_sequence')
        ]