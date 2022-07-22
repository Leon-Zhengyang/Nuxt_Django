from rest_framework import views, status
from rest_framework.permissions import IsAuthenticated
from app.models import Content
from apiv1.utils import success_resp
from collections import Counter, OrderedDict

class TagGetRankAPIView(views.APIView):
    """タグランキング取得"""

    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None, *args, **kwargs):
        contents = Content.objects.filter(deleted=0)
        tag_list = []
        for content in contents:
            tag_list.extend(content.tag.title().split())
        tag_obj = Counter(tag_list).most_common()[:10]
        return success_resp.create(tag_obj, status.HTTP_200_OK)
