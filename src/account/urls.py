from django.contrib import admin
from django.urls import path, include

from account.views import creation_compte, logout_user, login_user

app_name = "accounts"

urlpatterns = [
    path('signup/', creation_compte, name='signup'),
    path('logout/', logout_user, name='logout'),
    path('login/', login_user, name='login'),

]
