# Generated by Django 5.0.6 on 2024-06-16 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rps_game', '0010_remove_room_result1_remove_room_result2_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='round_result',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
