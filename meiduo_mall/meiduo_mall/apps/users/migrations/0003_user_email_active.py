# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2019-02-20 16:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20190220_0953'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email_active',
            field=models.BooleanField(default=False, verbose_name='邮箱签验证状态'),
        ),
    ]
