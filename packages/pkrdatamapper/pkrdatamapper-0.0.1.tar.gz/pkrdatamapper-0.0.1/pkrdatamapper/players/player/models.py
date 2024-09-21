from django.db import models

from pkrcomponents.components.players.table_player import TablePlayer

from pkrdatamapper.common.mixins import DFDataMixin


class DBPlayer(models.Model, DFDataMixin):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name

    @classmethod
    def from_table_player(cls, table_player: TablePlayer):
        db_player, _ = cls.objects.update_or_create(
            name=table_player.name,
        )
        return db_player

    class Meta:
        verbose_name = "Player"
        verbose_name_plural = "Players"
        ordering = ['name']
        db_table = 'players'