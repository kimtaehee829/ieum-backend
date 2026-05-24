from rest_framework import serializers
from .models import Post, Clue, Tag

class ClueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clue
        fields = ['id', 'file', 'created_at']

class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    clues = ClueSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'content', 'clues', 'created_at']