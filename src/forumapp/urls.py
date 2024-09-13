from django.contrib import admin
from django.urls import path
from forumapp.views import index
from forumapp.views import create_forum, signup_to_forum, connexion_to_forum, forum_slug, post_forum_messages, \
    message_reply_request, edit_message, delete_message, delete_sub_message

app_name = "forumapp"

urlpatterns = [
    path('', index, name="index"),
    path('create', create_forum, name="create_forum"),
    path('signup', signup_to_forum, name="signup_forum"),
    path('connexion_forum', connexion_to_forum, name="connexion_forum"),
    path('post_forums', post_forum_messages, name="post_forum_messages"),
    path('app/<str:slug>', forum_slug, name="forum_slug"),
    path('reply_message/<int:message_id>', message_reply_request, name="reply-form"),
    path('edit_message/<int:message_id>/', edit_message, name='edit_message'),
    path('delete_message/<int:message_id>/', delete_message, name='delete_message'),
    path('delete_sub_message/<int:reply_id>/', delete_sub_message, name='delete_sub_message')

]
