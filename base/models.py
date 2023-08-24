from ast import Delete

import os

from asyncio.windows_events import NULL
from email.policy import default
from email.quoprimime import body_check
from enum import unique
from random import choices
from time import timezone
from unittest.util import _MAX_LENGTH
from django.db import models
from django.urls import reverse

from django.db.models.signals import post_save, post_delete, pre_save

from django.dispatch import receiver

from django.core.files.storage import default_storage

from django.db.models.deletion import CASCADE

from datetime import datetime

from django.contrib.auth.models import AbstractBaseUser , BaseUserManager, PermissionsMixin

class UsersAccounts(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Please input your email')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.is_staff = False
        user.save(using=self._db)
        return user

    def create_superuser(self, email ,password=None):
        user = self.create_user(email, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user
    
    def get_by_natural_key(self, email_):
        return self.get(email=email_)
 
class User(AbstractBaseUser):
    USER_TYPES_CHOICES = (
        ('admin', 'Admin'),
        ('visitor', 'Visitor')
    )
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=100, unique=True)
    user_type = models.CharField(max_length=100, choices=USER_TYPES_CHOICES)
    is_active = models.BooleanField(default=True)
    created = models.DateField(auto_now=True)

    objects = UsersAccounts()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    ordering = ['-created']

    def __str__(self):
        return self.email

class BlogPost(models.Model):
    poster = models.ForeignKey(User,
        on_delete=models.CASCADE
    )

    image = models.ImageField(default='avatar.png', upload_to='images/posts')
    title = models.CharField(max_length=200)
    description = models.TextField()
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created', '-updated']

    def __str__(self):
        return self.title
    
class Profile(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        image = models.ImageField(default='avatar.png', upload_to='images/posts')
        name = models.CharField(max_length=100)
        bio = models.TextField()
        telephone = models.CharField(max_length=100)
        facebook = models.CharField(max_length=100, null=True)
        twitter = models.CharField(max_length=100, null=True)
        instagram = models.CharField(max_length=100, null=True)
        youtube = models.CharField(max_length=100, null=True)

        def __str__(self):
            return self.name


