from django.db import models

from applications.base.models import BaseMoneyModel
from applications.billings import BillingLineCategory, SettlementStatus
from applications.travels.models import Travel, Member
from applications.users.models import User


class Billing(BaseMoneyModel):
    travel = models.ForeignKey(Travel, related_name='billings', on_delete=models.CASCADE)
    title = models.CharField(max_length=31)
    image = models.ImageField()
    category = models.CharField(max_length=15, choices=BillingLineCategory.CHOICES, default=BillingLineCategory.FOOD)
    status = models.CharField(max_length=31, choices=SettlementStatus.CHOICES, default=SettlementStatus.NOT_CHARGED)
    paid_by = models.ForeignKey(User, related_name='billing_lines', on_delete=models.CASCADE)
    paid_date = models.DateField()

    @property
    def remaining_amount(self):
        return self.total_amount.amount - self.captured_amount.amount


class Settlement(BaseMoneyModel):
    billing = models.ForeignKey(Billing, related_name='settlements', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='settlements', on_delete=models.CASCADE)
    status = models.CharField(max_length=31, choices=SettlementStatus.CHOICES, default=SettlementStatus.NOT_CHARGED)

    @property
    def remaining_amount(self):
        return self.total_amount.amount - self.captured_amount.amount
