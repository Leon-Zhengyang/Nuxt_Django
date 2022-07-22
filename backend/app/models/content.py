from app.models.timestamped import Timestamped

from django.db import models

class Content(Timestamped):
    """コンテンツテーブル"""
    class Meta:
        db_table = "content"

    id = models.AutoField(primary_key=True)
    title = models.CharField("タイトル", max_length=50)
    text = models.TextField("本文")
    tag = models.CharField("タグ", blank=True, null=True, max_length=50)
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="contents")
    like_count = models.IntegerField("いいね数", default=0,)
    comment_count = models.IntegerField("コメント数", default=0,)
    deleted = models.IntegerField(
        choices=(
            (0, "ACTIVE"),
            (1, "INACTIVE"),
        ),
        default=0,
    )
