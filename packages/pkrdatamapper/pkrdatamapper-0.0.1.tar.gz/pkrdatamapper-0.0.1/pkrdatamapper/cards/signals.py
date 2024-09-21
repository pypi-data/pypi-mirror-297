from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver

from .card.models import DBCard
from .combo.models import DBCombo
from .flop.models import DBFlop
from .hand.models import DBHand
from .rank.models import DBRank
from .shape.models import DBShape
from .suit.models import DBSuit

@receiver(pre_save, sender=DBSuit)
@receiver(pre_delete, sender=DBSuit)
@receiver(pre_save, sender=DBRank)
@receiver(pre_delete, sender=DBRank)
@receiver(pre_save, sender=DBCard)
@receiver(pre_delete, sender=DBCard)
@receiver(pre_save, sender=DBShape)
@receiver(pre_delete, sender=DBShape)
@receiver(pre_save, sender=DBHand)
@receiver(pre_delete, sender=DBHand)
@receiver(pre_save, sender=DBCombo)
@receiver(pre_delete, sender=DBCombo)
@receiver(pre_save, sender=DBFlop)
@receiver(pre_delete, sender=DBFlop)
def protect_db_objects(sender, instance, **kwargs):
    if instance.pk:
        raise Exception("This object is protected and cannot be modified or deleted")
    