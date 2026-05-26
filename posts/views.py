from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Post, Clue, Tag
from .serializers import PostSerializer


class PostListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        posts = Post.objects.all()

        search_query = request.query_params.get('search', None)

        if search_query:
            posts = posts.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(tags__name__icontains=search_query)
            ).distinct()

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        title = request.data.get('title')
        content = request.data.get('content')
        files = request.FILES.getlist('clues')
        tags_data = request.data.getlist('tags')

        if len(files) > 3:
            return Response(
                {"error": "단서 사진은 최대 3장까지만 업로드할 수 있습니다."},
                status=status.HTTP_400_BAD_REQUEST
            )

        post = Post.objects.create(
            title=title,
            content=content,
            author=request.user
        )

        if tags_data:
            for tag_name in tags_data:
                tag_name = tag_name.strip()
                if tag_name:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    post.tags.add(tag)

        if files:
            for file in files:
                Clue.objects.create(post=post, file=file)

        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)