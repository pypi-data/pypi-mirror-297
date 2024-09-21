from django.db import models
from pkrdatamapper.common.mixins import DFDataMixin
from pkrcomponents.components.tournaments.buy_in import BuyIn


class DBBuyIn(models.Model, DFDataMixin):
    prize_pool_contribution = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    bounty = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    rake = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    total = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)

    def __repr__(self):
        return f"<BuyIn('{self.prize_pool_contribution:.2f}/{self.bounty:.2f}/{self.rake:.2f}')>"

    @classmethod
    def from_buy_in(cls, buy_in: BuyIn):
        db_buy_in, _ = cls.objects.get_or_create(
            prize_pool_contribution=buy_in.prize_pool,
            bounty=buy_in.bounty,
            rake=buy_in.rake,
            total=buy_in.total
        )
        db_buy_in.save()
        return db_buy_in

    @classmethod
    def from_total_buy_in(cls, total_buy_in: float):
        db_buy_in, _ = cls.objects.get_or_create(
            prize_pool_contribution=total_buy_in*0.9,
            rake=total_buy_in*0.1,
        )
        db_buy_in.save()
        return db_buy_in

    class Meta:
        db_table = 'buy_ins'
        verbose_name = "Buy In"
        verbose_name_plural = "Buy Ins"
        constraints = [
            models.UniqueConstraint(fields=['prize_pool_contribution', 'bounty', 'rake'], name='unique_buy_in')
        ]