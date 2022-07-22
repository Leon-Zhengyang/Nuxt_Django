from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import auth, user, content, comment, tag
from .views.user import UserViewSet
router = routers.DefaultRouter()
router.register(r"user-sets", UserViewSet)

app_name = "apiv1"
urlpatterns = [
    path("", include(router.urls)),
    # 認証関連
    path("token/", TokenObtainPairView.as_view()),
    path("auth/user/", auth.AuthUserAPIview.as_view()),
    # 使用者
    path("users/", user.UserCreateAPIView.as_view()),
    path("user-profile/<int:pk>", user.UserDetailUpdateAPIView.as_view()),
    path("user-follow/", user.UserFollowAPIView.as_view()),
    path("user-password/<int:pk>", user.UserPasswordAPIView.as_view()),
    # コンテンツ
    path("content/", content.ContentCreateAPIView.as_view()),
    path("content-image-url/", content.ContentCreateImageUrlAPIView.as_view()),
    path("content/<int:pk>", content.ContentGetUpdateAPIView.as_view()),
    path("content-self-all/", content.ContentSelfAllAPIView.as_view()),
    path("content-all/", content.ContentAllAPIView.as_view()),
    path("content-search/", content.ContentSearchAPIView.as_view()),
    path("content-great/<int:pk>", content.ContentGreatAPIView.as_view()),
    path("content-user-rank/", content.UserRankAPIView.as_view()),
    # コメント
    path("comment/", comment.CommentCreateAPIView.as_view()),
    path("comment-all/<int:pk>", comment.CommentAllAPIView.as_view()),
    # タグ
    path("tag-rank/", tag.TagGetRankAPIView.as_view()),
]