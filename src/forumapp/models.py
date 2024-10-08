from django.contrib.auth.models import AbstractUser
from django.db import models
from django.template.defaultfilters import slugify
from django.templatetags.static import static

from account.models import ForumUser


class Category(models.Model):
    nom = models.CharField(max_length=20)
    description = models.TextField(max_length=50)

    # identifiant_forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name="categories")

    def __str__(self):
        return f"{self.nom}"


class Forum(models.Model):
    nom = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField(max_length=100)
    date_created = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    identifiant_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="forums", default="")

    def __str__(self):
        return f"{self.slug}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)


class MemberForum(models.Model):
    user = models.ForeignKey(ForumUser, on_delete=models.CASCADE, related_name="users")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    avatar = models.ImageField(upload_to='photos/', blank=True)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name="forums")

    def __str__(self):
        return f"{self.user} {self.forum}"

    def __repr__(self):
        return f"MemberForum(user={self.user}, created_at={self.created_at}, updated_at={self.updated_at}," \
               f"forum={self.forum} )"

    def avatar_tag(self):
        return self.avatar.url if self.avatar else static("img/default.png")


class Thread(models.Model):
    name = models.CharField(max_length=20)
    created_by = models.ForeignKey(ForumUser, on_delete=models.CASCADE, related_name="threadss")
    identifiant_forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name="threads", default="1")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} {self.identifiant_forum}"


class Message(models.Model):
    titre = models.CharField(max_length=50)
    contenu = models.TextField(max_length=300)
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    posted_by = models.ForeignKey(ForumUser, on_delete=models.CASCADE, related_name="messages_users")
    thread_in = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="messages")
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    def __str__(self):
        return f"{self.titre}"
