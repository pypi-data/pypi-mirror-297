from django.db import models
from pkrcomponents.components.actions.street import Street
from pkrdatamapper.common.mixins import DFDataMixin


class DBStreet(models.Model, DFDataMixin):
    """Represents a street in poker"""

    name = models.CharField(max_length=10, unique=True)
    short_name = models.CharField(max_length=2, unique=True)
    parsing_name = models.CharField(max_length=10, unique=True)
    symbol = models.CharField(max_length=2, unique=True)
    is_preflop = models.BooleanField(default=False)

    def __repr__(self):
        return f"<DB_Street('{self.name}')>"

    @classmethod
    def from_street(cls, street: Street):
        db_street, _ = cls.objects.get_or_create(
            name=street.name,
            defaults={
                'short_name': street.short_name,
                'parsing_name': street.parsing_name,
                'symbol': street.symbol,
                'is_preflop': street.is_preflop
            }
        )
        return db_street

    @classmethod
    def objects_from_list(cls):
        if cls.objects.count() == len(Street):
            return cls.objects.all()
        return [cls.from_street(street) for street in list(Street)]

    class Meta:
        verbose_name = "Street"
        verbose_name_plural = "Streets"
        db_table = 'streets'
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_street')
        ]
