from django.urls import path
from apps.user_management.views import UserView, UserDetailView

urlpatterns = [
    path('users', UserView.as_view(), name='user_list_create'),
    path('users/<str:user_id>', UserDetailView.as_view(), name='user_detail'),
]
