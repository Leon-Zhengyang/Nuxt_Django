from rest_framework import views, status
from rest_framework.permissions import IsAuthenticated
from app.models import Content, User, Comment
from apiv1.serializers.comment import CommentSerializer
from apiv1.utils import success_resp
from django.shortcuts import get_object_or_404


class CommentCreateAPIView(views.APIView):
    """コメントするAPI"""

    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None, *args, **kwargs):
        request.data["from_user_id"] = request.data.pop("fromUserId")
        request.data["to_user_id"] = request.data.pop("toUserId")
        request.data["content_id"] = request.data.pop("contentId")
        serializer = CommentSerializer(context={"request": request}, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success_resp.create(serializer.data, status.HTTP_201_CREATED)

class CommentAllAPIView(views.APIView):
    """コメント一覧取得"""

    permission_classes = (IsAuthenticated,)
    
    def get(self, request, pk):
        content = get_object_or_404(Content, pk=pk)
        comments = Comment.objects.filter(content=content, deleted=0)
        serializer = CommentSerializer(comments, context={"request": request}, many=True)
        return success_resp.create(serializer.data, status.HTTP_200_OK)