from django.db import models
from django.conf import settings


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="태그명")

    class Meta:
        db_table = 'tags'

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts',
                               verbose_name="작성자")
    title = models.CharField(max_length=200, verbose_name="제목")
    content = models.TextField(verbose_name="내용")

    tags = models.ManyToManyField(Tag, related_name='posts', blank=True, verbose_name="태그")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="작성일")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일")

    class Meta:
        db_table = 'posts'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Clue(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='clues')

    file = models.FileField(upload_to='clues/%Y/%m/%d/', verbose_name="첨부파일")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="업로드일")

    class Meta:
        db_table = 'clues'

    def __str__(self):
        return f"{self.post.title}의 단서 파일"