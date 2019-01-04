# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-01-03 22:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fish_app2', '0003_auto_20190103_1351'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='games',
        ),
        migrations.AddField(
            model_name='player',
            name='game',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='players', to='fish_app2.Game'),
            preserve_default=False,
        ),
    ]
