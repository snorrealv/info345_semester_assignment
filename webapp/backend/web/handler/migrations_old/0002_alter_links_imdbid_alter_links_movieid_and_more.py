# Generated by Django 4.1 on 2022-08-18 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('handler', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='links',
            name='imdbId',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='links',
            name='movieId',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='links',
            name='tmdbId',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='movies',
            name='movieId',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='userrankings',
            name='movieId',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='userrankings',
            name='rank',
            field=models.IntegerField(),
        ),
    ]