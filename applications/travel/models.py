from django.db import models

# Create your models here.
from applications.base.models import BaseAdminModel
from applications.users.models import User


class Travel(BaseAdminModel):
    """
    여행 관련 Model 입니다.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="여행 리스트 방장")
    members = models.ManyToManyField(User, through="Member", related_name="members", verbose_name="여행 멤버들")
    title = models.CharField(max_length=255, verbose_name="여행 제목")
    start_date = models.DateField(verbose_name="여행 시작 날짜")
    end_date = models.DateField(verbose_name="여행 끝나는 날짜")
    description = models.CharField(max_length=13, verbose_name="여행 메모")

    def __str__(self):
        return self.title


class Member(BaseAdminModel):
    """
    여행에 참여한 멤버들 관련 Model 입니다.
    """
    user = models.ForeignKey(User, related_name="travel_member", on_delete=models.CASCADE, verbose_name="유저 FK")
    travel = models.ForeignKey(Travel, related_name="member", on_delete=models.CASCADE, verbose_name="여행 FK")
    is_admin = models.BooleanField(verbose_name="최고 관리자 여부")

    def __str__(self):
        return self.user.nickname
