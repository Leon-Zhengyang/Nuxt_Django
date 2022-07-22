from rest_framework import serializers
from django.contrib.auth import get_user_model
from app.models import User, Content, ProfileImage, ContentLike, ContentImage, Follows
from django.shortcuts import get_object_or_404
from apiv1.serializers.user import UserDetailSerializer

class ContentSerializer(serializers.ModelSerializer):

    created_user = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    modified_user = serializers.SerializerMethodField()
    modified_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    user_id = serializers.IntegerField()

    class Meta:
        model = Content
        fields = (
            "id",
            "user_id",
            "title",
            "text",
            "tag",
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
    
    def create(self, validated_data):
        user_id = validated_data["user_id"]
        user = get_object_or_404(User, pk=user_id)
        content = Content.objects.create(
            title=validated_data["title"],
            text=validated_data["text"],
            tag=validated_data["tag"],
            user=user,
            created_user=self.context.get("request").user,
        )
        return content

class ContentDetailUpdateSerializer(serializers.ModelSerializer):
    
    created_at = serializers.DateTimeField(format="%Y-%m-%d", required=False)
    modified_at = serializers.DateTimeField(format="%Y-%m-%d", required=False)
    isLiked = serializers.SerializerMethodField()
    isFollowed = serializers.SerializerMethodField()
    
    class Meta:
        model = Content
        fields = (
            "id",
            "like_count",
            "isLiked",
            "isFollowed",
            "tag",
            "title",
            "text",
            "created_at",
            "modified_at",
            "deleted",
        )
    
    def get_isLiked(self, obj):
        request = self.context.get('request')
        count = ContentLike.objects.filter(content=obj, user=request.user).count()
        if count > 0:
            return True
        else:
            return False
    
    def get_isFollowed(self, obj):
        request = self.context.get('request')
        request_user = request.user
        content_user = get_object_or_404(User, contents=obj, deleted=0)
        count = Follows.objects.filter(from_user=request_user, to_user=content_user).count()
        if count > 0:
            return True
        else:
            return False

class ContentSelfAllSerializer(serializers.ModelSerializer):
    
    created_at = serializers.DateTimeField(format="%Y-%m-%d", required=False)
    modified_at = serializers.DateTimeField(format="%Y-%m-%d", required=False)
    avatar_image = serializers.SerializerMethodField()
    avatar_initial = serializers.SerializerMethodField()
    
    class Meta:
        model = Content
        fields = (
            "id",
            "avatar_image",
            "avatar_initial",
            "like_count",
            "tag",
            "title",
            "text",
            "created_at",
            "modified_at",
            "deleted",
        )
        
    def get_avatar_image(self, obj):
        request = self.context.get('request')
        if not obj.user.profile_image.avatar_image:
            return None
        return request.build_absolute_uri(obj.user.profile_image.avatar_image.url)
    
    def get_avatar_initial(self, obj):
        if obj.user and obj.user.email:
            return obj.user.email[0].upper()
        return None

class ContentAllSerializer(serializers.ModelSerializer):
    
    created_at = serializers.DateTimeField(format="%Y-%m-%d", required=False)
    modified_at = serializers.DateTimeField(format="%Y-%m-%d", required=False)
    avatar_image = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    avatar_initial = serializers.SerializerMethodField()

    class Meta:
        model = Content
        fields = (
            "id",
            "user",
            "tag",
            "like_count",
            "avatar_image",
            "avatar_initial",
            "title",
            "text",
            "created_at",
            "modified_at",
            "deleted",
        )

    def get_avatar_image(self, obj):
        request = self.context.get('request')
        if not obj.user.profile_image.avatar_image or not obj.user.profile_image:
            return None
        return request.build_absolute_uri(obj.user.profile_image.avatar_image.url)

    def get_user(self, obj):
        if obj.user:
            return {"user_id":obj.user.id, "user_name":obj.user.name}
        return None

    def get_avatar_initial(self, obj):
        if obj.user and obj.user.email:
            return obj.user.email[0].upper()
        return None

class ContentImageCreateSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    
    class Meta:
        model = ContentImage
        fields = (
            "id",
            "image",
            "url",
        )
        extra_kwargs = {
            'image': {'write_only': True},
        }
    
    def create(self, validated_data):
        request = self.context.get('request')
        contentImage = ContentImage.objects.create(
            user=request.user,
            image=validated_data["image"],
        )
        contentImage.save()
        url = request.build_absolute_uri(contentImage.image.url)
        return contentImage
    
    def get_url(self, obj):
        request = self.context.get('request')
        url = request.build_absolute_uri(obj.image.url)
        return url