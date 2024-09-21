from django.db import models
from pkrcomponents.components.actions.action_move import ActionMove
from pkrdatamapper.common.mixins import DFDataMixin


class DBActionMove(models.Model, DFDataMixin):
    name = models.CharField(max_length=5, unique=True, db_comment="Name of the action move")
    symbol = models.CharField(max_length=1, unique=True, db_comment="Symbol of the action move")
    verb = models.CharField(max_length=6, unique=True, db_comment="Verb of the action move")
    is_call_move = models.BooleanField(default=False, db_comment="True if the action move is a call move")
    is_bet_move = models.BooleanField(default=False, db_comment="True if the action move is a bet move")
    is_vpip_move = models.BooleanField(default=False, db_comment="True if the action move is a VPIP move")

    def __str__(self):
        return self.name

    @classmethod
    def from_action_move(cls, action_move: ActionMove):
        if not action_move:
            return None
        db_action_move, _ = cls.objects.get_or_create(
            name=action_move.name,
            defaults={
                'symbol': action_move.symbol,
                'verb': action_move.verb,
                'is_call_move': action_move.is_call_move,
                'is_bet_move': action_move.is_bet_move,
                'is_vpip_move': action_move.is_vpip_move,
            }
        )
        return db_action_move

    @classmethod
    def objects_from_list(cls):
        if cls.objects.count() == 5:
            return cls.objects.all()
        return [cls.from_action_move(action_move) for action_move in list(ActionMove)[:5]]

    class Meta:
        verbose_name = "Action Move"
        verbose_name_plural = "Action Moves"
        db_table = 'action_moves'
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_action_move')
        ]
