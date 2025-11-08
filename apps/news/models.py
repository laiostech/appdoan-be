from django.db import models
import uuid

from apps.user_management.models import User

def generate_news_id():
    return f"news-{uuid.uuid4()}"
def generate_react_id():    
    return f"react-{uuid.uuid4()}"

class News(models.Model):
    id = models.CharField(primary_key=True, max_length=50, default=generate_news_id, editable=False)
    title = models.CharField(max_length=255)
    summary = models.TextField(blank=True, null=True)  # Tóm tắt nội dung
    content = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=30)


class Reaction(models.Model):
    id = models.CharField(primary_key=True, max_length=50, default=generate_react_id, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
