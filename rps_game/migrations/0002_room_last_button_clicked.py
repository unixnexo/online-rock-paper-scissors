# Generated by Django 5.0.6 on 2024-06-13 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rps_game', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='last_button_clicked',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
