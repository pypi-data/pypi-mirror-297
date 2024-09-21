from django.db import models
from pkrcomponents.components.actions.blind_type import BlindType
from pkrdatamapper.common.mixins import DFDataMixin


class DBBlindType(models.Model, DFDataMixin):
    name = models.CharField(max_length=16, unique=True)
    symbol = models.CharField(max_length=2, unique=True)

    def __str__(self):
        return self.name

    @classmethod
    def from_blind_type(cls, blind_type: BlindType):
        db_blind_type, _ = cls.objects.get_or_create(
            name=blind_type.name,
            defaults={
                'symbol': blind_type.symbol
            }
        )
        return db_blind_type

    @classmethod
    def objects_from_list(cls):
        if cls.objects.count() == len(BlindType):
            return cls.objects.all()
        return [cls.from_blind_type(blind_type) for blind_type in list(BlindType)]

    class Meta:
        verbose_name = "Blind Type"
        verbose_name_plural = "Blind Types"
        db_table = 'blind_types'
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_blind_type')
        ]
