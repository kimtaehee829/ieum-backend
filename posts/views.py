from django.core.exceptions import ValidationError
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import Post, Clue, Tag
from .serializers import PostListSerializer, PostSerializer
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.http import HttpResponse
import urllib.parse
from django.http import FileResponse

class PostListCreateView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        posts = Post.objects.all()

        tag_names = request.GET.getlist('tag')
        if tag_names:
            posts = posts.filter(tags__name__in=tag_names).distinct()

        search_query = request.GET.get('search')
        if search_query:
            posts = posts.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(tags__name__icontains=search_query)
            ).distinct()

        ordering = request.GET.get('ordering', 'newest')
        if ordering == 'oldest':
            posts = posts.order_by('created_at')
        else:
            posts = posts.order_by('-created_at')

        serializer = PostListSerializer(posts, many=True, context={'request': request})
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

        for file in files:
            ext = file.name.split('.')[-1].lower()
            size_limit = 0

            if ext in ['jpg', 'jpeg', 'png', 'webp']:
                size_limit = 10 * 1024 * 1024
            elif ext in ['mp4', 'mov']:
                size_limit = 50 * 1024 * 1024
            elif ext in ['mp3', 'wav', 'm4a']:
                size_limit = 20 * 1024 * 1024

            if size_limit > 0 and file.size > size_limit:
                return Response(
                    {
                        "status": 413,
                        "error_code": "FILE_SIZE_EXCEEDED",
                        "message": f"파일 용량 제한을 초과했습니다. (현재 파일: {ext.upper()})",
                        "timestamp": timezone.now().strftime('%Y-%m-%dT%H:%M:%SZ')
                    },
                    status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
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

class PostDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, post_id):
        return get_object_or_404(Post, id=post_id)

    def get(self, request, post_id):
        post = self.get_object(post_id)
        serializer = PostSerializer(post, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, post_id):
        post = self.get_object(post_id)

        if post.author != request.user:
            raise PermissionDenied("게시글을 수정할 권한이 없습니다.")
        tags_data = request.data.get('tags')

        serializer = PostSerializer(post, data=request.data, partial=True)

        if serializer.is_valid():
            post_instance = serializer.save()

            if tags_data is not None:
                post_instance.tags.clear()

                if isinstance(tags_data, str):
                    tag_list = [tag.strip() for tag in tags_data.split(',') if tag.strip()]
                elif isinstance(tags_data, list):
                    tag_list = [tag.strip() for tag in tags_data if isinstance(tag, str) and tag.strip()]
                else:
                    tag_list = []

                for tag_name in tag_list:
                    tag, _ = Tag.objects.get_or_create(name=tag_name)
                    post_instance.tags.add(tag)

            updated_serializer = PostSerializer(post_instance, context={'request': request})
            return Response(
                {
                    "message": "게시글이 성공적으로 수정되었습니다.",
                    "data": updated_serializer.data
                },
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, post_id):
        post = self.get_object(post_id)

        if post.author != request.user:
            raise PermissionDenied("게시글을 삭제할 권한이 없습니다.")

        post.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class FileDownloadView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, _request, clue_id):
        clue = get_object_or_404(Clue, id=clue_id)

        try:
            file_handle = clue.file.open('rb')
        except Exception:
            return Response(
                {"error": "스토리지에서 파일을 찾을 수 없습니다."},
                status=status.HTTP_404_NOT_FOUND
            )

        original_filename = clue.file.name.split('/')[-1]

        encoded_filename = urllib.parse.quote(original_filename)

        response = FileResponse(file_handle, content_type='application/octet-stream')
        response['Content-Disposition'] = f"attachment; filename*=UTF-8''{encoded_filename}"

        return response