# Generated by Django 5.0.6 on 2024-07-09 09:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0002_rename_category_genres_rename_category_movie_genres_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='user',
        ),
        migrations.AlterField(
            model_name='movie',
            name='added_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.logintable'),
        ),
        migrations.AlterField(
            model_name='review',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.logintable'),
        ),
    ]
