from django.db import models
from pkrcomponents.components.cards.shape import Shape
from pkrdatamapper.common.mixins import DFDataMixin


class DBShape(models.Model, DFDataMixin):
    name = models.CharField(max_length=8, unique=True)
    short_name = models.CharField(max_length=2, unique=True)
    symbol = models.CharField(max_length=2, unique=True)

    def __str__(self):
        return f"{self.short_name}"

    @classmethod
    def from_shape(cls, shape: Shape):
        try:
            db_shape = cls.objects.get(short_name=shape.symbol)
        except cls.DoesNotExist:
            db_shape = cls(
                name=shape.name,
                short_name=shape.symbol,
                symbol=shape.symbol,
            )
            db_shape.save()
        return db_shape

    @classmethod
    def objects_from_list(cls):
        if cls.objects.count() == len(Shape):
            return cls.objects.all()
        return [cls.from_shape(shape) for shape in list(Shape)]

    class Meta:
        verbose_name = "Shape"
        verbose_name_plural = "Shapes"
        db_table = 'shapes'
        constraints = [
            models.UniqueConstraint(fields=['short_name'], name='unique_shape')
        ]
