from django.db import models


class BaseAdminModel(models.Model):
    """
    created, updated로 구성된 기본 Base Model입니다.
    """
    created = models.DateTimeField(auto_now_add=True, verbose_name="생성일")
    updated = models.DateTimeField(auto_now=True, verbose_name="수정일")

    class Meta:
        abstract = True


class Currency(models.Model):
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=100)
    rate = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class BaseMoneyModel(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    captured_amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        abstract = True
