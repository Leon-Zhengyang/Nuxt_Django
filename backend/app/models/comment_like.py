from app.models.timestamped import Timestamped

from django.db import models

class CommentLike(Timestamped):
    """コメントいいねテーブル"""
    class Meta:
        db_table = "comment_like"

    id = models.AutoField(primary_key=True)
    comment = models.ForeignKey("Comment", on_delete=models.CASCADE, related_name="like")
    from_user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="comment_like")