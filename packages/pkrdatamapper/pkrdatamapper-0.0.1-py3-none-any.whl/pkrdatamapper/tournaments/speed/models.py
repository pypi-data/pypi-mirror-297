from django.db import models
from pkrcomponents.components.tournaments.speed import TourSpeed
from pkrdatamapper.common.mixins import DFDataMixin


class DBTourSpeed(models.Model, DFDataMixin):
    name = models.CharField(max_length=8, unique=True, db_comment="The speed of the tournament")

    def __str__(self):
        return self.name

    @classmethod
    def from_tour_speed(cls, tour_speed: TourSpeed):
        db_tour_speed, _ = cls.objects.get_or_create(
            name=tour_speed.name,
        )
        return db_tour_speed

    @classmethod
    def objects_from_list(cls):
        if cls.objects.count() == len(TourSpeed):
            return cls.objects.all()
        return [cls.from_tour_speed(tour_speed) for tour_speed in list(TourSpeed)]

    class Meta:
        db_table = 'tour_speeds'
        verbose_name = "Tournament Speed"
        verbose_name_plural = "Tournament Speeds"
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_tour_speed')
        ]
