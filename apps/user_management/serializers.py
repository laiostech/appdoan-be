from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User

class UserSerializer(serializers.ModelSerializer):
    role_display = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'full_name', 'unit', 'role', 'role_display', 'date_of_birth', 'joining_date']
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'required': True},
            'full_name': {'required': True},
            'username': {'required': True},
            'date_of_birth': {'required': True},
            'joining_date': {'required': True}
        }

    def create(self, validated_data):
        # Hash password trước khi lưu
        validated_data['password'] = make_password(validated_data.get('password'))
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Hash password nếu được cập nhật
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data.get('password'))
        return super().update(instance, validated_data)