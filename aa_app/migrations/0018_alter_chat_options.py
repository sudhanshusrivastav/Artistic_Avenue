# Generated by Django 5.0.4 on 2024-05-06 10:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aa_app', '0017_alter_chat_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chat',
            options={'ordering': ['-created']},
        ),
    ]
