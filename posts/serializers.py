from rest_framework import serializers
from .models import Post, Clue, Tag

class ClueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clue
        fields = ['id', 'file', 'created_at']

class PostSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'  # Tag 모델의 'name' 필드만 쏙 빼옵니다.
    )
    author = serializers.ReadOnlyField(source='author.username')
    clues = ClueSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'content', 'tags', 'clues', 'created_at']