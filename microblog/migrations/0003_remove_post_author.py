# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-04-26 21:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('microblog', '0002_post_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='author',
        ),
    ]
