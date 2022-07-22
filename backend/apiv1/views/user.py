from django.contrib.auth.models import Permission
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status, views, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser
from django.http import QueryDict
from django.db import transaction
from django.contrib.auth.hashers import check_password

from apiv1.serializers.user import (
    UserDetailSerializer, 
    UserUpdateSerializer,
    ProfileImageUpdateSerializer,
    UserCreateSerializer,
    UserSetSerializer,
)
from apiv1.utils import success_resp

from app.models import User, ProfileImage, Follows


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(deleted=0)
    serializer_class = UserSetSerializer


class UserCreateAPIView(views.APIView):
    """新規アカウント作成"""

    def post(self, request, format=None, *args, **kwargs):
        serializer = UserCreateSerializer(context={"request": request}, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success_resp.create(serializer.data, status.HTTP_201_CREATED)

class UserPasswordAPIView(views.APIView):
    """ユーザーパスワード更新API"""
    def put(self, request, pk, format=None, *args, **kwargs):
        user = get_object_or_404(User, pk=pk, deleted=0)
        oldPassword = request.data.pop('oldPassword')
        if check_password(oldPassword,user.password):
            pass
        return success_resp.create(status.HTTP_200_OK)

class UserDetailUpdateAPIView(views.APIView):
    """ユーザー情報詳細・更新API"""
    parser_classes = (MultiPartParser,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, format=None, *args, **kwargs):
        """ユーザー情報詳細取得メソッド"""
        user = get_object_or_404(User, pk=pk, deleted=0)
        serializer = UserDetailSerializer(user, context={"request": request})
        return success_resp.create(serializer.data, status.HTTP_200_OK)
    
    @transaction.atomic
    def put(self, request, pk, format=None, *args, **kwargs):
        """ユーザー情報更新メソッド"""
        user = get_object_or_404(User, pk=pk, deleted=0)
        profile_image = ProfileImage.objects.get(user=user)
        user_data = request.data.copy()
        avatar_image={"avatar_image" : None}
        if not type(user_data["avatar_image"]) is str:
            avatar_image["avatar_image"] = user_data.pop("avatar_image")[0]

        # ユーザー情報更新
        serializer = UserUpdateSerializer(instance=user, context={"request":request}, data=user_data)
        serializer.is_valid(raise_exception=True)
        serializer.save(modified_user=request.user)
        # プロフィール画像更新
        if not avatar_image["avatar_image"] is None:
            serializer_profile = ProfileImageUpdateSerializer(instance=profile_image, context={"request": request}, data=avatar_image)
            serializer_profile.is_valid(raise_exception=True)
            serializer_profile.save(modified_user=request.user)
        return success_resp.create(serializer.data, status.HTTP_200_OK)
    
class UserFollowAPIView(views.APIView):
    """ユーザーフォローAPI"""
    permission_classes = (IsAuthenticated,)

    @classmethod
    def __isFollowed(self, request):
        count = Follows.objects.filter(
                from_user_id=request.data['fromUserId'],
                to_user_id=request.data['toUserId'],
            ).count()
        if count > 0:
            return True
        else:
            return False

    def post(self, request, format=None, *args, **kwargs):
        from_user = get_object_or_404(User, pk=request.data['fromUserId'], deleted=0)
        to_user = get_object_or_404(User, pk=request.data['toUserId'], deleted=0)
        is_followed = self.__isFollowed(request)
        if is_followed == False:
            Follows.objects.create(
                from_user=from_user,
                to_user=to_user,
            )
        else:
            follow = Follows.objects.get(
                from_user=from_user,
                to_user=to_user,
            )
            follow.delete()
        return success_resp.create(status.HTTP_200_OK)
    
    