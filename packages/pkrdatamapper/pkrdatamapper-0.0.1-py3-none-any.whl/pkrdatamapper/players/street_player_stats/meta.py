"""This module contains the metaclass for the database stats models."""
from django.db import models
from pkrdatamapper.common.fields import CountField
from pkrdatamapper.histories.street_player_hand_stats.base import DBStreetPlayerHandStats

class DBPlayerStatsMeta(type):

    associated_model: DBStreetPlayerHandStats

    def __init__(cls, name, bases, dct):
        super(DBPlayerStatsMeta, cls).__init__(name, bases, dct)
        if not cls._meta.abstract:
            cls.setup_fields()

    def get_flag_fields(cls):
        return [field for field in cls.associated_model._meta.fields if field.name.startswith("flag_")]

    def setup_fields(cls):
        flag_fields = cls.get_flag_fields()
        for flag_field in flag_fields:
            cls.generate_count_from_flag_field(flag_field)

    def generate_count_from_flag_field(cls, flag_field):
        count_field_name = flag_field.name.replace("flag_", "cnt_")
        count_field = CountField(
            associated_flag=flag_field,
            associated_model=cls.associated_model,
            name=count_field_name,
            db_column=count_field_name,
            db_comment=f"Count of hands where {flag_field.db_comment.replace('Whether ', ' ')}",
            default=0
        )
        count_field.contribute_to_class(cls, count_field_name)