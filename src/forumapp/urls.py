from django.contrib import admin
from django.urls import path
from forumapp.views import index
from forumapp.views import create_forum, signup_to_forum, connexion_to_forum, forum_slug, post_forum_messages

app_name = "forumapp"

urlpatterns = [
    path('', index, name="index"),
    path('create', create_forum, name="create_forum"),
    path('signup', signup_to_forum, name="signup_forum"),
    path('connexion_forum', connexion_to_forum, name="connexion_forum"),
    path('<str:slug>', forum_slug, name="forum_slug"),
    path('post_forum', post_forum_messages, name="post_forum_messages")
]
