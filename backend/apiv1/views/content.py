from ast import keyword
from rest_framework import views, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser
from app.models import Content, User, ContentLike
from apiv1.serializers.content import ContentSerializer, ContentAllSerializer, ContentDetailUpdateSerializer, UserDetailSerializer, ContentImageCreateSerializer
from apiv1.utils import success_resp
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.db.models import Count


class ContentCreateAPIView(views.APIView):
    """コンテンツ登録"""

    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None, *args, **kwargs):
        request.data["user_id"] = request.data.pop("userId")
        serializer = ContentSerializer(context={"request": request}, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success_resp.create(serializer.data, status.HTTP_201_CREATED)

class ContentCreateImageUrlAPIView(views.APIView):
    """markdownにアップロードした図のURLを生成する"""
    parser_classes = (MultiPartParser,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None, *args, **kwargs):
        request.data["image"] = request.data.pop("imgFile")[0]
        serializer = ContentImageCreateSerializer(context={"request": request}, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success_resp.create(serializer.data, status.HTTP_200_OK)

class ContentGetUpdateAPIView(views.APIView):
    """コンテンツ詳細・編集・削除"""

    permission_classes = (IsAuthenticated,)

    def get(self, request, pk,format=None, *args, **kwargs):
        content = get_object_or_404(Content, pk=pk)

        serializer = ContentDetailUpdateSerializer(content, context={"request": request})
        return success_resp.create(serializer.data, status.HTTP_200_OK)
    
    def put(self, request, pk,format=None, *args, **kwargs):
        content = get_object_or_404(Content, pk=pk)
        request.data.pop("contentId")
        serializer = ContentDetailUpdateSerializer(instance=content, context={"request":request}, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(modified_user=request.user)
        return success_resp.create(serializer.data, status.HTTP_200_OK)

class ContentSelfAllAPIView(views.APIView):
    """自分の投稿したコンテンツ一覧取得"""

    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        return getAll(request)

class ContentAllAPIView(views.APIView):
    """投稿されたコンテンツ一覧取得"""

    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        return getAll(request)

class ContentSearchAPIView(views.APIView):
    """投稿したコンテンツ検索"""

    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        return getAll(request)

def getAll(request):
    """コンテンツ一覧取得メソッド"""

    q_condition = Q()
    if 'userId' in request.data:
        user = get_object_or_404(User, pk=request.data['userId'], deleted=0)
        if 'flag' in request.data:
            if request.data['flag'] == 0:
                q_condition = Q(user=user)
            if request.data['flag'] == 1:
                q_condition = Q(like__user=user)
            if request.data['flag'] == 2:
                q_condition = Q(comments__from_user=user)

    if "keyword" in request.data and request.data["keyword"]:
        keyword = request.data["keyword"]
        q_condition = Q(title__icontains=keyword) | Q(text__icontains=keyword) | Q(tag__icontains=keyword)
    
    order_by = "-id"
    if "sort" in request.data and request.data["sort"]:
        order_by = request.data["sort"]

    contents = Content.objects.filter(q_condition, deleted=0).order_by(order_by).distinct()
    serializer = ContentAllSerializer(contents, context={"request": request}, many=True)
    return success_resp.create(serializer.data, status.HTTP_200_OK)

class ContentGreatAPIView(views.APIView):
    """いいねAPI"""

    permission_classes = (IsAuthenticated,)

    def post(self, request, pk, format=None, *args, **kwargs):
        content = get_object_or_404(Content, pk=pk, deleted=0)
        count = ContentLike.objects.filter(
                user_id=request.data['userId'],
                content_id=request.data['contentId'],
            ).count()
        if request.data['good'] == True:
            if count > 0:
                return success_resp.create(status.HTTP_200_OK)
            else:
                ContentLike.objects.create(
                    user_id=request.data['userId'],
                    content_id=request.data['contentId'],
                )
                content.like_count += 1
        else:
            if content.like_count > 0:
                content.like_count -= 1
            if count > 0:
                content_like = ContentLike.objects.get(
                    user_id=request.data['userId'],
                    content_id=request.data['contentId'],
                )
                content_like.delete()
        content.save()
        return success_resp.create(status.HTTP_200_OK)
    
class UserRankAPIView(views.APIView):
    """ユーザー投稿ランキング取得"""

    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None, *args, **kwargs):
        count_users = Content.objects.filter(deleted=0).values('user_id').annotate(count = Count('user_id'))
        return_list = []
        for count_user in count_users:
            user = User.objects.get(pk=count_user["user_id"])
            serializer = UserDetailSerializer(user, context={"request": request})
            serializer.data["content_count"] = count_user["count"]
            return_list.append(serializer.data)
        return success_resp.create(return_list, status.HTTP_200_OK)
