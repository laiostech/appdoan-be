# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import uuid

def generate_user_id():
    return f"user-{uuid.uuid4()}"

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(username, password, **extra_fields)

class User(AbstractBaseUser):
    # Các trường cần thiết
    id = models.CharField(primary_key=True, max_length=50, default=generate_user_id, editable=False)
    username = models.CharField(max_length=150, unique=True)
    full_name = models.CharField(max_length=255, verbose_name='Full Name', null=True, blank=True)
    date_of_birth = models.DateField(verbose_name='Date of Birth', null=True, blank=True)
    joining_date = models.DateField(verbose_name='Joining Date', null=True, blank=True)
    unit = models.CharField(max_length=255, verbose_name='Unit', blank=True, null=True)
    role = models.CharField(
        max_length=20,
        choices=[
            ('doan-vien', 'Đoàn viên'),
            ('can-bo', 'Cán bộ quản lý Đoàn')
        ],
        default='doan-vien'
    )
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # Các thuộc tính cần thiết cho custom user model
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['full_name']

    objects = UserManager()

    class Meta:
        db_table = 'user_management_user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.full_name} ({self.get_role_display()})"

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
