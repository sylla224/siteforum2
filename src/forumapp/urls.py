from django.contrib import admin
from django.urls import path
from forumapp.views import index

app_name = "forumapp"

urlpatterns = [
    path('', index, name="index"),
]
