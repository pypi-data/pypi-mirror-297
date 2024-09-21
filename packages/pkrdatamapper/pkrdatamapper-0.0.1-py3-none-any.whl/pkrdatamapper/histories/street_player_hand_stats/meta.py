from django.db import models
from pkrdatamapper.actions.action_move.models import DBActionMove
from pkrdatamapper.actions.actions_sequence.models import DBActionsSequence
from pkrdatamapper.histories.street_player_hand_stats.datafields.base import data_type_mapper


class DBHandStatsMeta(type):

    data_attr_fields: list
    data_fields: list

    def __init__(cls, name, bases, dct):
        super(DBHandStatsMeta, cls).__init__(name, bases, dct)
        if not cls._meta.abstract:
            cls.setup_fields()

    def setup_fields(cls):
        cls.data_fields = [cls.set_data_field_from_attr(attr_field) for attr_field in cls.data_attr_fields]
        for field in cls.data_fields:
            field.contribute_to_class(cls, field.name)

    def set_data_field_from_attr(cls, attr_field):
        field_name = attr_field.get("field_name")
        data_field_name = field_name.lower()
        field_var = attr_field.get("field_var")
        description = field_var.metadata.get("description")
        field_type = field_var.metadata.get("type")
        field_default = field_var._default
        field_nullable = field_default is None
        associated_model = data_type_mapper.get(field_type)
        try:
            if field_type == "decimal_15_2":
                new_field = models.DecimalField(
                    default=field_default,
                    verbose_name=data_field_name,
                    name=data_field_name,
                    null=field_nullable,
                    max_digits=15,
                    decimal_places=2,
                    db_comment=description,
                    db_column=data_field_name
                )
            elif field_type == "decimal_10_5":
                new_field = models.DecimalField(
                    default=field_default,
                    verbose_name=data_field_name,
                    name=data_field_name,
                    null=field_nullable,
                    max_digits=10,
                    decimal_places=5,
                    db_comment=description,
                    db_column=data_field_name
                )
            elif not issubclass(associated_model, models.Model):
                new_field = associated_model(
                    default=field_default,
                    verbose_name=data_field_name,
                    name=data_field_name,
                    null=field_nullable,
                    db_comment=description,
                    db_column=data_field_name
                )
            else:
                new_field = models.ForeignKey(
                    associated_model,
                    on_delete=models.DO_NOTHING,
                    null=field_nullable,
                    related_name=f"{f'{cls.prefix}_' if associated_model in {DBActionMove, DBActionsSequence} else ''}"
                                 f"{data_field_name}",
                    verbose_name=data_field_name,
                    name=data_field_name,
                    db_comment=description,
                    db_column=data_field_name,
                )
            return new_field
        except TypeError:
            print(f"Field {field_name} with type {field_type} not supported")
            raise TypeError
