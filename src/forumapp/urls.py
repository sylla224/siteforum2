from django.contrib import admin
from django.urls import path
from forumapp.views import index
from forumapp.views import create_forum

app_name = "forumapp"

urlpatterns = [
    path('', index, name="index"),
    path('create', create_forum, name="create_forum"),
]
