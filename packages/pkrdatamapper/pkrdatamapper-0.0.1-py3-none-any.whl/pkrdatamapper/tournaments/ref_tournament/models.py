from django.db import models



from pkrcomponents.components.tables.table import Table
from pkrcomponents.components.tournaments.tournament import Tournament
from pkrdatamapper.common.mixins import DFDataMixin
from pkrdatamapper.tournaments.buy_in.models import DBBuyIn
from pkrdatamapper.tournaments.speed.models import DBTourSpeed
from pkrdatamapper.tournaments.type.models import DBTourType


class DBRefTournament(models.Model, DFDataMixin):

    name = models.CharField(max_length=64, db_comment="The name of the tournament")
    buy_in = models.ForeignKey(DBBuyIn, on_delete=models.CASCADE, db_comment="The buy-in of the tournament")
    speed = models.ForeignKey(DBTourSpeed, on_delete=models.CASCADE, db_comment="The speed of the tournament",
                              default=2)
    starting_stack = models.IntegerField(default=20000, db_comment="The starting stack of the players")
    is_ko = models.BooleanField(default=False, db_comment="Whether the tournament is a knockout")
    tournament_type = models.ForeignKey(DBTourType, on_delete=models.CASCADE, db_comment="The type of the tournament",
                                        default=1)

    @classmethod
    def from_tournament(cls, tournament: Tournament):
        buy_in = DBBuyIn.from_buy_in(tournament.buy_in)
        tour_type = DBTourType.from_tour_type(tournament.tournament_type)
        speed = DBTourSpeed.from_tour_speed(tournament.speed)
        db_ref_tournament, _ = cls.objects.update_or_create(
            name=tournament.name,
            buy_in=buy_in,
            speed=speed,
            starting_stack=tournament.starting_stack,
            is_ko=tournament.is_ko,
            tournament_type=tour_type,

        )
        return db_ref_tournament

    @classmethod
    def from_table(cls, table: Table):
        ref_tournament = cls.objects.get_or_create(
            name=table.tournament.name,
            buy_in__total=table.total_buy_in).first()
        return ref_tournament

    @classmethod
    def estimate_buy_in(cls, table: Table):
        # Get reference tournaments with the same name and buy-in
        ref_tournaments = cls.objects.filter(name=table.tournament.name, buy_in__total=table.total_buy_in)
        print(ref_tournaments)
        # Among these, select the most common buy-in
        buy_ins = ref_tournaments
        print(buy_ins)
        buy_in = ref_tournaments.values('buy_in').annotate(count=models.Count('buy_in')).order_by('-count').first()
        # Return the buy-in
        return buy_in

    class Meta:
        db_table = 'ref_tournaments'
        verbose_name = "Reference Tournament"
        verbose_name_plural = "Reference Tournaments"
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'buy_in', 'speed', 'starting_stack', 'tournament_type'],
                name='unique_ref_tournament')
        ]
