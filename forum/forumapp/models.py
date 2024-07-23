from django.contrib.auth.models import AbstractUser
from django.db import models


class ForumUser(AbstractUser):
    username = None
    email = models.EmailField(max_length=240, unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Forum(models.Model):
    nom = models.CharField(max_length=50)
    description = models.TextField(max_length=100)
    date_created = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class Category(models.Model):
    nom = models.CharField(max_length=20)
    description = models.TextField(max_length=50)
    identifiant_forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name="categories")


class Thread(models.Model):
    created_by = models.ForeignKey(ForumUser, on_delete=models.CASCADE, related_name="threads")
    identifiant_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="threads")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    titre = models.CharField(max_length=50)
    contenu = models.TextField(max_length=300)
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    posted_by = models.ForeignKey(ForumUser, on_delete=models.CASCADE, related_name="messages_users")
    thread_in = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="messages")
