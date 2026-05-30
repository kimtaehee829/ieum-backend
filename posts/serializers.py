from rest_framework import serializers
from .models import Post, Clue, Tag

class ClueSerializer(serializers.ModelSerializer):
    clue_id = serializers.IntegerField(source='id', read_only=True)
    file_url = serializers.FileField(source='file')
    file_type = serializers.SerializerMethodField()

    class Meta:
        model = Clue
        fields = ['clue_id', 'file_type', 'file_url']

    def get_file_type(self, obj):
        if not obj.file:
            return 'UNKNOWN'

        ext = obj.file.name.split('.')[-1].lower()
        if ext in ['jpg', 'jpeg', 'png', 'webp']:
            return 'IMAGE'
        elif ext in ['mp4', 'mov']:
            return 'VIDEO'
        elif ext in ['mp3', 'wav', 'm4a']:
            return 'AUDIO'
        return 'UNKNOWN'

class PostSerializer(serializers.ModelSerializer):
    post_id = serializers.IntegerField(source='id', read_only=True)
    author_username = serializers.CharField(source='author.username', read_only=True)
    sns_link = serializers.CharField(source='author.sns_link', read_only=True)

    tags = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')

    clues = ClueSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['post_id', 'author_username', 'title', 'content', 'sns_link', 'tags', 'clues', 'created_at', 'updated_at']

class PostListSerializer(serializers.ModelSerializer):
    post_id = serializers.IntegerField(source='id', read_only=True)
    author_username = serializers.CharField(source='author.username', read_only=True)
    thumbnail_url = serializers.SerializerMethodField()

    tags = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Post
        fields = ['post_id', 'author_username', 'title', 'tags', 'created_at', 'thumbnail_url']

    def get_thumbnail_url(self, obj):
        first_clue = obj.clues.first()

        if first_clue and first_clue.file:
            return first_clue.file.url

        return None