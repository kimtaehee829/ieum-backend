from django.urls import path
from .views import SignupView, ProfileView, MyPostsView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/me/', ProfileView.as_view(), name='profile-me'),
    path('profile/me/posts/', MyPostsView.as_view(), name='my-posts'),
]