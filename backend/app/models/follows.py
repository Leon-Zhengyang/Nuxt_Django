from app.models.timestamped import Timestamped

from django.db import models

class Follows(Timestamped):
    """フォローテーブル"""
    class Meta:
        db_table = "follow"

    id = models.AutoField(primary_key=True)
    # フォローしているユーザー
    from_user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="follows")
    # フォローされているユーザー
    to_user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="followers")


