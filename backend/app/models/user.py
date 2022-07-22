from distutils.command.build_scripts import first_line_re
import uuid

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils import timezone

from app.models.timestamped import Timestamped
from app.utils.const import UserType


class UserManager(BaseUserManager):
    """カスタムユーザーマネージャーモデル"""

    use_in_migrations = True

    def _create_user(self, name, email, password=None, **extra_fields):
        if not name:
            raise ValueError("名前は必須です")
        if not email:
            raise ValueError("emailは必須です")
        email = self.normalize_email(email)
        name = self.model.normalize_username(name)
        user = self.model(name=name, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, name, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(name, email, password, **extra_fields)

    def create_superuser(self, name, email, password, **extra_fields):
        extra_fields.setdefault("user_type", 9)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")
        return self._create_user(name, email, password, **extra_fields)

def image_upload_path(instance, filename):
    """ユーザープロフィール画像保存先パスを生成
    "/image_profile/ユーザーID"
    """
    return "image/image_profile/{}".format(
        instance.id,
    )

class User(AbstractBaseUser, PermissionsMixin, Timestamped):
    """ユーザー"""

    id = models.AutoField(primary_key=True)
    name = models.CharField("名前", max_length=50, null=True, blank=True)
    birthday = models.DateField("生年月日(西暦)", null=True, blank=True)
    email = models.EmailField("メールアドレス", unique=True, max_length=50)
    user_type = models.IntegerField("ユーザータイプ", choices=UserType.choices(), default=1)
    sex = models.IntegerField(
        "性別",
        choices=(
            (0, "woman"),
            (1, "man"),
            (9, "others"),
        ),
        default=0,
    )
    biography = models.TextField(
        "自己紹介",
        blank=True,
        null=True,
        max_length=255,
    )
    deleted = models.IntegerField(
        "削除フラグ",
        choices=(
            (0, "ACTIVE"),
            (1, "INACTIVE"),
        ),
        default=0,
    )
    is_staff = models.BooleanField("is_staff", default=False)
    is_active = models.BooleanField("is_active", default=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    @property
    def is_nomal_user(self):
        try:
            return self.user_type == UserType.USER.value
        except ObjectDoesNotExist:
            return True

    @property
    def is_system_manager(self):
        try:
            return self.user_type == UserType.SUPERUSER.value and not bool(self.is_nomal_user)
        except ObjectDoesNotExist:
            return True

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        db_table = "user"
