from rest_framework import serializers
from .models import News, Reaction

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'

class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = '__all__'

class NewsWithReactionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    content = serializers.CharField()
    create_at = serializers.DateTimeField()
    update_at = serializers.DateTimeField()
    category = serializers.CharField()
    reaction_count = serializers.IntegerField()

class ImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField()

class ImageDeleteSerializer(serializers.Serializer):
    ids = serializers.ListField(
        child=serializers.CharField(), allow_empty=False
    )