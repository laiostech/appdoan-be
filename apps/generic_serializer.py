from rest_framework import serializers

class MessageResponseSerializer(serializers.Serializer):
    message = serializers.CharField()

class ErrorResponseSerializer(serializers.Serializer):
    detail = serializers.CharField()