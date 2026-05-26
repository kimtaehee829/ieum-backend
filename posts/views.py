from django.core.exceptions import ValidationError
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Post, Clue, Tag
from .serializers import PostListSerializer

class PostListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        search_query = request.query_params.get('search', '')

        if search_query:
            posts = Post.objects.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(tags__name__icontains=search_query)
            ).distinct()
        else:
            posts = Post.objects.all()

        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        title = request.data.get('title')
        content = request.data.get('content')
        files = request.FILES.getlist('clues')

        tags_string = request.data.get('tags', '')

        if len(files) > 3:
            return Response(
                {
                    "status": 400,
                    "error_code": "MAX_FILE_COUNT_EXCEEDED",
                    "message": "첨부 파일이 3개를 초과했습니다.",
                    "timestamp": timezone.now().strftime('%Y-%m-%dT%H:%M:%SZ')
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        post = Post.objects.create(
            title=title,
            content=content,
            author=request.user
        )

        if tags_string:
            tag_names = [tag.strip() for tag in tags_string.split(',') if tag.strip()]

            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                post.tags.add(tag)

        if files:
            for file in files:
                clue = Clue(post=post, file=file)
                try:
                    clue.full_clean()
                    clue.save()
                except ValidationError as e:
                    post.delete()

                    return Response(
                        {
                            "status": 400,
                            "error_code": "INVALID_EXTENSION",
                            "message": "지원하지 않는 파일 확장자입니다.",
                            "timestamp": timezone.now().strftime('%Y-%m-%dT%H:%M:%SZ')
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

        return Response(
            {
                "post_id": post.id,
                "message": "게시글이 성공적으로 등록되었습니다."
            },
            status=status.HTTP_201_CREATED
        )