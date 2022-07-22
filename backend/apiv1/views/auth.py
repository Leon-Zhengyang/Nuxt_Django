from rest_framework import views
from rest_framework.permissions import IsAuthenticated

from apiv1.serializers.auth import AuthUserSerializer
from apiv1.utils import success_resp


class AuthUserAPIview(views.APIView):
    """ログインユーザー情報取得API"""

    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        serializer = AuthUserSerializer(self.request.user, context={"request": request})
        return success_resp.create(serializer.data)
