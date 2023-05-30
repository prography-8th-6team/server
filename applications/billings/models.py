from django.db import models

from applications.base.models import BaseMoneyModel
from applications.billings import BillingLineCategory, SettlementStatus
from applications.travel.models import Travel, Member
from applications.users.models import User


class Billing(BaseMoneyModel):
    travel = models.ForeignKey(Travel, related_name='billings', on_delete=models.CASCADE)
    title = models.CharField(max_length=31)
    image = models.ImageField()
    category = models.CharField(max_length=15, choices=BillingLineCategory.CHOICES, default=BillingLineCategory.FOOD)
    paid_by = models.ForeignKey(Member, related_name='billing_lines', on_delete=models.CASCADE)
    paid_date = models.DateField()


class Settlement(BaseMoneyModel):
    billing = models.ForeignKey(Billing, related_name='settlements', on_delete=models.CASCADE)
    member = models.ForeignKey(Member, related_name='settlements', on_delete=models.CASCADE)
    status = models.CharField(max_length=31, choices=SettlementStatus.CHOICES, default=SettlementStatus.NOT_CHARGED)
