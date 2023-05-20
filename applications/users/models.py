from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models

# Create your models here.
from applications.base.models import BaseAdminModel


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, nickname, password=None, **kwargs):

        if not nickname:
            raise ValueError('must have user nickname')

        user = self.model(
            nickname=nickname,
            **kwargs,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, nickname, password=None, **kwargs):

        user = self.create_user(
            nickname=nickname,
            password=password,
            **kwargs,
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, BaseAdminModel):
    """
    User Model 입니다.
    """
    # TODO : social id = 숫자로 할 것인지, 문자로 할 것인지 (카카오는 숫자 대충 10자리, 네이버는 문자열)
    objects = UserManager()

    nickname = models.CharField(max_length=255, unique=True, verbose_name="별명")
    social_id = models.CharField(max_length=255, verbose_name="소셜 로그인 아이디")
    email = models.CharField(max_length=255, unique=True, null=True, verbose_name="이메일")
    fcm_token = models.CharField(max_length=255, null=True, verbose_name="FCM Token")
    is_admin = models.BooleanField(default=False, verbose_name="관리자 권한")

    USERNAME_FIELD = 'nickname'

    def __str__(self):
        return self.nickname

    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin
