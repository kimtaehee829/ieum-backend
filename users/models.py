from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    sns_link = models.URLField(max_length=500, blank=True, null=True, help_text="연락 가능한 SNS 링크")

    class Meta:
        db_table = 'users'
        verbose_name = '사용자'
        verbose_name_plural = '사용자 목록'

    def __str__(self):
        return self.username