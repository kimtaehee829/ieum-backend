from django.urls import path
from .views import PostListCreateView, PostDetailView, FileDownloadView

urlpatterns = [
    path('', PostListCreateView.as_view(), name='post_list_create'),
    path('<int:post_id>/', PostDetailView.as_view(), name='post-detail'),
    path('clues/<int:clue_id>/download/', FileDownloadView.as_view(), name='file-download'),
]