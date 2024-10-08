# Generated by Django 5.0.7 on 2024-08-28 12:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forumapp', '0003_memberforum'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='thread',
            name='identifiant_category',
        ),
        migrations.AddField(
            model_name='thread',
            name='identifiant_forum',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='threads', to='forumapp.forum'),
        ),
        migrations.AlterField(
            model_name='thread',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='threadss', to=settings.AUTH_USER_MODEL),
        ),
    ]
