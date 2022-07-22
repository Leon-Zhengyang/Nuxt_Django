from app.models.timestamped import Timestamped
from django.core.exceptions import ObjectDoesNotExist

from django.db import models
import os.path

def image_upload_path(instance, filename):
    notExistFlag = False
    try:
        instance.content
    except ObjectDoesNotExist:
        notExistFlag = True
    _, ext = os.path.splitext(filename)

    return "image/image_content/{0}/{1}{2}".format(
        instance.user.id,
        instance.content.id if hasattr(instance.content,'id') or notExistFlag else 0,
        ext,
    )

class ContentImage(Timestamped):
    """コンテンツテーブル"""
    class Meta:
        db_table = "content_image"

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user_content_images")
    content = models.ForeignKey("Content", on_delete=models.SET_NULL, null=True, blank=True, related_name="contents")
    image = models.ImageField("コンテンツ画像",upload_to=image_upload_path)
    deleted = models.IntegerField(
        choices=(
            (0, "ACTIVE"),
            (1, "INACTIVE"),
        ),
        default=0,
    )
