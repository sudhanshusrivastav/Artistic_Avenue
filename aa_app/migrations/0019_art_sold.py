# Generated by Django 5.0.4 on 2024-05-06 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aa_app', '0018_alter_chat_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='art',
            name='sold',
            field=models.BooleanField(default=False),
        ),
    ]
