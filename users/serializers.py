from rest_framework import serializers
from django.contrib.auth import get_user_model
from posts.models import Post

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'sns_link')

        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            sns_link=validated_data.get('sns_link', '')
        )
        return user

class ProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='id', read_only=True)
    created_at = serializers.DateTimeField(source='date_joined', read_only=True)

    class Meta:
        model = User
        fields = ['user_id', 'username', 'sns_link', 'created_at']
        read_only_fields = ['username']

class MyPostListSerializer(serializers.ModelSerializer):
    # 명세서 요구사항에 맞게 id를 post_id로 매핑
    post_id = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = Post
        fields = ['post_id', 'title', 'created_at']