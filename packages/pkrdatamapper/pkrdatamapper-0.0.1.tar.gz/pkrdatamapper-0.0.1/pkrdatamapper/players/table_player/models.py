from django.db import models
from pkrcomponents.components.players.table_player import TablePlayer

from ..player.models import DBPlayer
from ..position.models import DBPosition
from pkrdatamapper.cards.combo.models import DBCombo
from pkrdatamapper.histories.hand_history.models import DBHandHistory


class DBTablePlayer(models.Model):
    hand_history = models.ForeignKey(DBHandHistory, on_delete=models.CASCADE)
    player = models.ForeignKey(DBPlayer, on_delete=models.CASCADE)
    seat = models.PositiveSmallIntegerField()
    init_stack = models.DecimalField(decimal_places=2, max_digits=12, default=0.0)
    bounty = models.DecimalField(decimal_places=2, max_digits=9, default=0.0)
    combo = models.ForeignKey(DBCombo, on_delete=models.DO_NOTHING, null=True)
    position = models.ForeignKey(DBPosition, on_delete=models.DO_NOTHING, null=True)
    is_hero = models.BooleanField(default=False)

    @classmethod
    def from_table_player(cls, table_player: TablePlayer):
        player = DBPlayer.from_table_player(table_player)
        hand_history = DBHandHistory.from_table(table_player.table)
        combo = DBCombo.from_combo(table_player.combo)
        position = DBPosition.from_position(table_player.position)
        db_table_player, _ = cls.objects.get_or_create(
            hand_history=hand_history,
            player=player,
            defaults={
                'seat': table_player.seat,
                'init_stack': table_player.stack,
                'bounty': table_player.bounty,
                'combo': combo,
                'position': position,
                'is_hero': table_player.is_hero
            }
        )
        return db_table_player

    class Meta:
        unique_together = ('hand_history', 'player')
        ordering = ['hand_history', 'seat']
        db_table = 'table_players'

