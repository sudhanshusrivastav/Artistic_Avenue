# Generated by Django 5.0.4 on 2024-05-06 09:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aa_app', '0015_delete_chat'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_message', models.TextField(blank=True, null=True)),
                ('artist_message', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='aa_app.artist')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='aa_app.user')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]
