from pkrcomponents.components.players.datafields.postflop import POSTFLOP_FIELDS
from pkrdatamapper.histories.street_player_hand_stats.datafields.base import set_data_field_from_attr

POSTFLOP_DATA_FIELDS = [set_data_field_from_attr(attr_field) for attr_field in POSTFLOP_FIELDS]