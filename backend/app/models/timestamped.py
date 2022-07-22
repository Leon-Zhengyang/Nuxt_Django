from django.db import models


class Timestamped(models.Model):
    """created,modifiedフィールドを追加する抽象クラス"""

    class Meta:
        abstract = True

    created_user = models.ForeignKey(
        "User", on_delete=models.SET_NULL, null=True, related_name="%(class)s_created_user"
    )
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    modified_user = models.ForeignKey(
        "User", on_delete=models.SET_NULL, null=True, related_name="%(class)s_modified_user"
    )
    modified_at = models.DateTimeField(null=True, auto_now=True)
