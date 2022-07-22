from rest_framework import serializers

from app.models import User


class AuthUserSerializer(serializers.ModelSerializer):
    
    avatar_image = serializers.SerializerMethodField()
    avatar_initial = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = (
            "id",
            "name",
            "user_type",
            "avatar_image",
            "avatar_initial",
        )
    
    def get_avatar_image(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.profile_image.avatar_image.url) if obj.profile_image.avatar_image else None

    def get_avatar_initial(self, obj):
        if obj.email:
            return obj.email[0].upper()
        return None