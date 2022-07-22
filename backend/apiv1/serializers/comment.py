from rest_framework import serializers
from django.contrib.auth import get_user_model
from app.models import User, Content, Comment
from django.shortcuts import get_object_or_404
from apiv1.serializers.user import UserDetailSerializer


class CommentSerializer(serializers.ModelSerializer):
    
    created_user = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    modified_user = serializers.SerializerMethodField()
    modified_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    from_user_id = serializers.IntegerField()
    to_user_id = serializers.IntegerField()
    content_id = serializers.IntegerField()
    from_user_avatar_image = serializers.SerializerMethodField()
    from_user_avatar_initial = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            "id",
            "from_user_id",
            "to_user_id",
            "content_id",
            "from_user_avatar_image",
            "from_user_avatar_initial",
            "comment",
            "created_user",
            "created_at",
            "modified_user",
            "modified_at",
            "deleted",
        )
    
    def get_created_user(self, obj):
        if obj.created_user is None:
            return {"user_id": None, "name": None}
        return {"user_id": obj.created_user.id, "name": obj.created_user.name}

    def get_modified_user(self, obj):
        if obj.modified_user is None:
            return {"user_id": None, "name": None}
        return {"user_id": obj.modified_user.id, "name": obj.modified_user.name}
    
    def get_from_user_avatar_image(self, obj):
        request = self.context.get('request')
        if not obj.from_user.profile_image.avatar_image:
            return None
        return request.build_absolute_uri(obj.from_user.profile_image.avatar_image.url)

    def get_from_user_avatar_initial(self, obj):
        if obj.from_user and obj.from_user.email:
            return obj.from_user.email[0].upper()
        return None

    def create(self, validated_data):
        from_user_id = validated_data["from_user_id"]
        to_user_id = validated_data["to_user_id"]
        content_id = validated_data["content_id"]
        from_user = get_object_or_404(User, pk=from_user_id)
        to_user = get_object_or_404(User, pk=to_user_id)
        content = get_object_or_404(Content, pk=content_id)
        comment = Comment.objects.create(
            from_user=from_user,
            to_user=to_user,
            content=content,
            comment=validated_data["comment"],
            created_user=self.context.get("request").user,
        )
        return comment