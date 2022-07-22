import os
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models, transaction
from app.models.timestamped import Timestamped

def image_upload_path(instance, filename):
    """ユーザープロフィール画像保存先パスを生成
    "/image_profile/ユーザーID/version.拡張子"
    """
    _, ext = os.path.splitext(filename)
    return "image/image_profile/{0}/{1}{2}".format(
        instance.id,
        instance.image_version,
        ext,
    )

class ProfileImage(Timestamped):
    """プロフィール"""
    class Meta:
        db_table = "profile_image"

    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(
        "User",
        on_delete=models.CASCADE,
        related_name="profile_image",
    )
    avatar_image = models.ImageField(
        "プロフィール画像",
        upload_to=image_upload_path,
        null=True,
        blank=True,
    )
    image_version = models.IntegerField("画像バージョン", default=0)
    deleted = models.BooleanField("削除フラグ", default=False)
    
    # def save(self, *args, **kwargs):
    #     saved_avatar_image = self.avatar_image
    #     # self.avatar_image = None
    #     # super().save(*args, **kwargs)
    #     self.avatar_image = saved_avatar_image
    #     if "force_insert" in kwargs:
    #         kwargs.pop("force_insert")
    #     super().save(*args, **kwargs)