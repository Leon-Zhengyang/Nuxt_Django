from app.models.timestamped import Timestamped

from django.db import models

class ContentLike(Timestamped):
    """コンテンツいいねテーブル"""
    class Meta:
        db_table = "content_like"

    id = models.AutoField(primary_key=True)
    content = models.ForeignKey("Content", on_delete=models.CASCADE, related_name="like")
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="like")