from django.db import models


class BaseAdminModel(models.Model):
    """
    created, updated로 구성된 기본 Base Model입니다.
    """
    created = models.DateTimeField(auto_now_add=True, verbose_name="생성일")
    updated = models.DateTimeField(auto_now=True, verbose_name="수정일")

    class Meta:
        abstract = True
