from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
import os

from app.models import User, ProfileImage, Follows, Content

class UserSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("name", "email", "created_at")

class UserCreateSerializer(serializers.ModelSerializer):

    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    modified_user = serializers.SerializerMethodField()
    modified_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    email = serializers.EmailField(validators=[UniqueValidator(queryset=get_user_model().objects.all())])
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "name",
            "birthday",
            "email",
            "password",
            "deleted",
            "created_at",
            "modified_user",
            "modified_at",
            "sex",
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
        user = User(
            name=validated_data["name"],
            birthday=validated_data["birthday"],
            email=validated_data["email"],
            sex=validated_data["sex"],
            is_staff=1,
            is_active=1,
        )
        user.set_password(validated_data["password"])
        user.save()
        ProfileImage.objects.create(
            user=user
        )
        return user

    def delete(self, instance, modified_user):
        instance.deleted = 1
        instance.modified_user = modified_user
        instance.save()
        return instance

class UserUpdateSerializer(serializers.ModelSerializer):
    
    created_user = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    modified_user = serializers.SerializerMethodField()
    modified_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)

    class Meta:
        model = User
        fields = (
            "id",
            "name",
            "birthday",
            "deleted",
            "created_user",
            "created_at",
            "modified_user",
            "modified_at",
            "user_type",
            "biography",
            "sex",
        )

    def get_created_user(self, obj):
        if obj.created_user is None:
            return {"user_id": None, "name": None}
        return {"user_id": obj.created_user.id, "name": obj.created_user.name}

    def get_modified_user(self, obj):
        if obj.modified_user is None:
            return {"user_id": None, "name": None}
        return {"user_id": obj.modified_user.id, "name": obj.modified_user.name}

    def update(self, instance, validated_data):
        instance.name = validated_data["name"]
        instance.sex = validated_data["sex"]
        instance.birthday = validated_data["birthday"]
        instance.biography = validated_data["biography"]
        if "email" in validated_data:
            instance.email = validated_data["email"]
        if "password" in validated_data:
            instance.set_password(validated_data["password"])
        instance.modified_user = self.context.get("request").user
        instance.save()
        return instance


class UserDetailSerializer(serializers.ModelSerializer):
    """ユーザー情報詳細シリアライザー"""
    
    created_user = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    modified_user = serializers.SerializerMethodField()
    modified_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    user_type = serializers.SerializerMethodField()
    sex = serializers.SerializerMethodField()
    avatar_image = serializers.SerializerMethodField()
    avatar_initial = serializers.SerializerMethodField()
    follow_user_count = serializers.SerializerMethodField()
    followed_user_count = serializers.SerializerMethodField()
    isFollowed = serializers.SerializerMethodField()
    content_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "name",
            "avatar_image",
            "avatar_initial",
            "follow_user_count",
            "followed_user_count",
            "isFollowed",
            "content_count",
            "deleted",
            "created_user",
            "created_at",
            "modified_user",
            "modified_at",
            "user_type",
            "biography",
            "sex",
            "birthday",
        )

    def get_created_user(self, obj):
        if obj.created_user is None:
            return {"user_id": None, "name": None}
        return {"user_id": obj.created_user.id, "name": obj.created_user.name}

    def get_modified_user(self, obj):
        if obj.modified_user is None:
            return {"user_id": None, "name": None}
        return {"user_id": obj.modified_user.id, "name": obj.modified_user.name}

    def get_follow_user_count(self, obj):
        return Follows.objects.filter(from_user=obj).count()
    
    def get_followed_user_count(self, obj):
        return Follows.objects.filter(to_user=obj).count()

    def get_isFollowed(self, obj):
        request = self.context.get('request')
        request_user = request.user
        count = Follows.objects.filter(from_user=request_user, to_user=obj).count()
        if count > 0:
            return True
        else:
            return False

    def get_content_count(self, obj):
        return Content.objects.filter(user=obj).count()

    def get_user_type(self, obj):
        if obj.user_type is None:
            return {"id": None, "name": None}
        return {"id": str(obj.user_type), "name": obj.get_user_type_display()}

    def get_sex(self, obj):
        return str(obj.sex)
    
    def get_avatar_image(self, obj):
        request = self.context.get('request')
        if obj.profile_image.avatar_image:  
            return request.build_absolute_uri(obj.profile_image.avatar_image.url)
        return None

    def get_avatar_initial(self, obj):
        if obj.email:
            return obj.email[0].upper()
        return None

class ProfileImageUpdateSerializer(serializers.ModelSerializer):
    """プロフィール画像更新シリアライザー"""
    
    created_user = serializers.SerializerMethodField("get_created_user")
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    modified_user = serializers.SerializerMethodField("get_modified_user")
    modified_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    
    class Meta:
        model = ProfileImage
        fields = (
            "id",
            "avatar_image",
            "deleted",
            "created_user",
            "created_at",
            "modified_user",
            "modified_at",
        )
    
    def get_created_user(self, obj):
        if obj.created_user is None:
            return {"user_id": None, "name": None}
        return {"user_id": obj.created_user.id, "name": obj.created_user.name}

    def get_modified_user(self, obj):
        if obj.modified_user is None:
            return {"user_id": None, "name": None}
        return {"user_id": obj.modified_user.id, "name": obj.modified_user.name}

    def update(self, instance, validated_data):
        # if instance.image_version > 0:
        #     os.remove('/code/backend/media/image/image_profile/' + str(instance.id) +'.png')
        instance.avatar_image = validated_data["avatar_image"]
        instance.image_version += 1
        instance.save()
        return instance