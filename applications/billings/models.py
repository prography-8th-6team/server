from django.db import models

from applications.base.models import BaseMoneyModel
from applications.billings import BillingLineCategory, PaymentStatus
from applications.travel.models import Travel, Member


class Billing(BaseMoneyModel):
    travel = models.ForeignKey(Travel, related_name='billings', on_delete=models.CASCADE)


class SubBilling(BaseMoneyModel):
    member = models.ForeignKey(Member, related_name='sub_billings', on_delete=models.CASCADE)
    travel = models.ForeignKey(Travel, related_name='sub_billings', on_delete=models.CASCADE)


class BillingLine(BaseMoneyModel):
    sub_billing = models.ForeignKey(SubBilling, related_name='billing_lines', on_delete=models.CASCADE)
    image = models.ImageField()
    category = models.CharField(max_length=15, choices=BillingLineCategory.CHOICES, default=BillingLineCategory.FOOD)
    paid_by = models.ForeignKey(Member, related_name='billing_lines', on_delete=models.CASCADE)
    paid_date = models.DateField()


class Settlement(BaseMoneyModel):
    billing_line = models.ForeignKey(BillingLine, related_name='settlements', on_delete=models.CASCADE)
    member = models.ForeignKey(Member, related_name='settlements', on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=PaymentStatus.CHOICES, default=PaymentStatus.NOT_CHARGED)
