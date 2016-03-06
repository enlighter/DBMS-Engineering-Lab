# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-03-06 09:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courseSystem', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accomplishment',
            name='student',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='courseSystem.Learners'),
        ),
        migrations.AlterField(
            model_name='performance',
            name='student',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='courseSystem.Learners'),
        ),
    ]
