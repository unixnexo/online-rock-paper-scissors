# Generated by Django 5.0.6 on 2024-06-17 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rps_game', '0014_remove_room_player1_viewed_result_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='all_moves',
            field=models.TextField(default='[]'),
        ),
    ]
