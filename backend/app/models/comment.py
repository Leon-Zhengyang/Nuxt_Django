from app.models.timestamped import Timestamped

from django.db import models

class Comment(Timestamped):
    """コメントテーブル"""
    class Meta:
        db_table = "comment"

    id = models.AutoField(primary_key=True)
    from_user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="send_comments")
    to_user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="receive_comments")
    content = models.ForeignKey("Content", on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField(
        "コメント内容",
        blank=True,
        null=True,
        max_length=255,
    )
    like_count = models.IntegerField("いいね数", blank=True, null=True)
    deleted = models.IntegerField(
        choices=(
            (0, "ACTIVE"),
            (1, "INACTIVE"),
        ),
        default=0,
    )
