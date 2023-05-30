from django.db import models
from djmoney.models.fields import MoneyField


class BaseAdminModel(models.Model):
    """
    created, updated로 구성된 기본 Base Model입니다.
    """
    created = models.DateTimeField(auto_now_add=True, verbose_name="생성일")
    updated = models.DateTimeField(auto_now=True, verbose_name="수정일")

    class Meta:
        abstract = True


class BaseMoneyModel(models.Model):
    total_amount = MoneyField(max_digits=10, decimal_places=2, default_currency='USD', default=0)
    captured_amount = MoneyField(max_digits=10, decimal_places=2, default_currency='USD', default=0)

    class Meta:
        abstract = True
