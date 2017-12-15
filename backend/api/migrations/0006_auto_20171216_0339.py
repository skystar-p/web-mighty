# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-15 18:39
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_room_player_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamehistory',
            name='friend',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='friend_histories', to=settings.AUTH_USER_MODEL),
        ),
    ]
