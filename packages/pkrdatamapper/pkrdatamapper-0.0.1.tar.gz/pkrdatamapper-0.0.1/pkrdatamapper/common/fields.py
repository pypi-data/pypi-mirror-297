from botocore.handlers import handle_service_name_alias
from django.db.models import PositiveIntegerField, BooleanField, Model
from pkrdatamapper.histories.player_hand_stats.models import DBPlayerHandStats

class CountField(PositiveIntegerField):
    """
    A custom PositiveIntegerField to store the count of True occurences for a specific flag.
    """
    def __init__(self,associated_model=None, associated_flag=None, *args, **kwargs):

        self.associated_model = associated_model
        self.associated_flag = associated_flag
        super().__init__(*args, **kwargs)
        
    def calculate_count(self, instance) -> int:
        print(f"Calculating count for {instance.player.name}'s {self.associated_flag.name if self.associated_flag else 'hands'}")
        stat_to_analyse = self.associated_model.objects.filter(player=instance.player)
        if self.associated_flag:
            stat_to_analyse = stat_to_analyse.filter(**{self.associated_flag.name: True})
        count_value = stat_to_analyse.count()
        return count_value

    def pre_save(self, model_instance, add):
        count_value = self.calculate_count(model_instance)
        setattr(model_instance, self.attname, count_value)
        return count_value

        