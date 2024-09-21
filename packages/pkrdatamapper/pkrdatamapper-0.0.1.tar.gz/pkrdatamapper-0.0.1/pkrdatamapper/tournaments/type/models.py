from django.db import models
from pkrcomponents.components.tournaments.tournament_type import TournamentType
from pkrdatamapper.common.mixins import DFDataMixin


class DBTourType(models.Model, DFDataMixin):
    name = models.CharField(max_length=16, unique=True, db_comment="The type of the tournament")

    def __str__(self):
        return self.name

    @classmethod
    def from_tour_type(cls, tour_type: TournamentType):
        db_tour_type, _ = cls.objects.get_or_create(
            name=tour_type.name,
        )
        return db_tour_type

    @classmethod
    def objects_from_list(cls):
        if cls.objects.count() == len(TournamentType):
            return cls.objects.all()
        return [cls.from_tour_type(tour_type) for tour_type in list(TournamentType)]

    class Meta:
        db_table = 'tour_types'
        verbose_name = "Tournament Type"
        verbose_name_plural = "Tournament Types"
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_tour_type')
        ]
