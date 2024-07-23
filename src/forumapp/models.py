from django.contrib.auth.models import AbstractUser
from django.db import models
from django.template.defaultfilters import slugify

from src.account.models import ForumUser


class Forum(models.Model):
    nom = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField(max_length=100)
    date_created = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)


class Category(models.Model):
    nom = models.CharField(max_length=20)
    description = models.TextField(max_length=50)
    identifiant_forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name="categories")

    def __str__(self):
        return f"{self.nom}"


class Thread(models.Model):
    name = models.CharField(max_length=20)
    created_by = models.ForeignKey(ForumUser, on_delete=models.CASCADE, related_name="threads")
    identifiant_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="threads")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} {self.identifiant_category}"


class Message(models.Model):
    titre = models.CharField(max_length=50)
    contenu = models.TextField(max_length=300)
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    posted_by = models.ForeignKey(ForumUser, on_delete=models.CASCADE, related_name="messages_users")
    thread_in = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="messages")

    def __str__(self):
        return f"{self.titre}"
