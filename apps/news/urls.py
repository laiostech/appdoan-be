from django.urls import path
from apps.news.views import NewsAllListView, NewsByCategoryView, NewsDetailView, ImageUploadView, ImageBatchDeleteView, ImageServeView

urlpatterns = [
    path('news', NewsAllListView.as_view()),
    path('news/<str:news_id>', NewsDetailView.as_view()),
    path('news/category/<str:category>', NewsByCategoryView.as_view()),
    path('images/upload', ImageUploadView.as_view()),
    path('images/delete', ImageBatchDeleteView.as_view()),
    path('images/<str:filename>', ImageServeView.as_view()),
]
