# Generated by Django 2.1.2 on 2018-11-03 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_auto_20181021_2005'),
    ]

    operations = [
        migrations.AddField(
            model_name='gamesessionmessage',
            name='type',
            field=models.TextField(default='message', max_length=10),
        ),
    ]
