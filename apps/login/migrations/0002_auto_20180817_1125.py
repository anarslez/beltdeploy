# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-08-17 16:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wish',
            name='granter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='grants', to='login.User'),
        ),
    ]
