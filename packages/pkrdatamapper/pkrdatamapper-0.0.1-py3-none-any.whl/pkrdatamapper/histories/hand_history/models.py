import pytz

from django.db import models
from django.conf import settings

from pkrcomponents.components.tables.table import Table

from pkrdatamapper.common.mixins import DFDataMixin

from pkrdatamapper.cards.card.models import DBCard
from pkrdatamapper.cards.combo.models import DBCombo
from pkrdatamapper.cards.flop.models import DBFlop
from pkrdatamapper.tournaments.buy_in.models import DBBuyIn
from pkrdatamapper.tournaments.level.models import DBLevel
from pkrdatamapper.tournaments.ref_tournament.models import DBRefTournament
from pkrdatamapper.tournaments.tournament.models import DBTournament


class DBHandHistory(models.Model, DFDataMixin):
    hand_id = models.CharField(max_length=64, unique=True, null=False, blank=True, default="")
    hand_date = models.DateTimeField()
    tournament = models.ForeignKey(DBTournament, on_delete=models.DO_NOTHING)
    flop = models.ForeignKey(DBFlop, on_delete=models.DO_NOTHING, null=True)
    turn = models.ForeignKey(DBCard, on_delete=models.DO_NOTHING, related_name="turns", null=True)
    river = models.ForeignKey(DBCard, on_delete=models.DO_NOTHING, related_name="rivers", null=True)
    max_players = models.PositiveSmallIntegerField()
    cnt_players = models.PositiveSmallIntegerField()
    button_seat = models.PositiveSmallIntegerField()
    level = models.ForeignKey(DBLevel, on_delete=models.DO_NOTHING)
    hero_combo = models.ForeignKey(DBCombo, on_delete=models.DO_NOTHING, null=True)

    @classmethod
    def estimate_ref_tournament(cls, table: Table):
        """"""
        ref_tournaments = DBTournament.objects.filter(
            ref_tournament__name=table.tournament.name,
            ref_tournament__buy_in__total=table.total_buy_in
        ).values('ref_tournament').annotate(count=models.Count('ref_tournament')).order_by('-count')
        try:
            ref_tournament = ref_tournaments.first().get("ref_tournament")
            return DBRefTournament.objects.get(pk=ref_tournament)
        except AttributeError:
            buy_in = DBBuyIn.from_total_buy_in(table.total_buy_in)
            db_ref_tournament, _ = DBRefTournament.objects.get_or_create(
                name=table.tournament.name,
                buy_in=buy_in)
            return db_ref_tournament


    @classmethod
    def estimate_tournament(cls, table: Table):
        """
        Estimate the tournament object from the table
        """
        db_tournament = DBTournament.objects.filter(tournament_id=table.tournament.id).first()
        if not db_tournament:
            ref_tournament = cls.estimate_ref_tournament(table)
            tournaments = DBTournament.objects.filter(ref_tournament=ref_tournament)
            total_players_avg = tournaments.values('total_players').aggregate(models.Avg('total_players'))
            prize_pool_avg = tournaments.values('prize_pool').aggregate(models.Avg('prize_pool'))
            try:
                total_players = round(total_players_avg["total_players__avg"], 0)
                prize_pool = round(prize_pool_avg["prize_pool__avg"], 2)
            except TypeError:
                total_players, prize_pool = 180, 0.0
            local_timezone = pytz.timezone(settings.TIME_ZONE)
            start_date = local_timezone.localize(table.hand_date.replace(hour=0, minute=0, second=0, microsecond=0))
            db_tournament = DBTournament(
                tournament_id=table.tournament.id,
                ref_tournament=ref_tournament,
                total_players=total_players,
                prize_pool=prize_pool,
                start_date=start_date
            )
        db_tournament.save()
        return db_tournament

    @classmethod
    def from_table(cls, table: Table):
        tournament = cls.estimate_tournament(table)
        flop = DBFlop.from_flop(table.board.flop)
        turn = DBCard.from_card(table.board.turn)
        river = DBCard.from_card(table.board.river)
        level = DBLevel.from_level(table.level)
        hero_combo = DBCombo.from_combo(table.hero_combo)
        local_timezone = pytz.timezone(settings.TIME_ZONE)
        hand_date = local_timezone.localize(table.hand_date)
        db_hand_history, _ = cls.objects.update_or_create(
            hand_id=table.hand_id,
            defaults={
                'hand_date': hand_date,
                'tournament': tournament,
                'flop': flop,
                'turn': turn,
                'river': river,
                'max_players': table.max_players,
                'cnt_players': table.cnt_players,
                'button_seat': table.players.button_seat,
                'level': level,
                'hero_combo': hero_combo
            }
        )
        return db_hand_history

    class Meta:
        verbose_name = "Hand History"
        verbose_name_plural = "Hand Histories"
        ordering = ['hand_id', 'hand_date']
        db_table = 'hand_histories'
