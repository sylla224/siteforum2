from django.contrib import admin
from account.models import ForumUser
from forumapp.models import Thread, Category, Message, Forum

# Register your models here.

admin.site.register(Thread)
admin.site.register(Category)
admin.site.register(Message)
admin.site.register(Forum)
