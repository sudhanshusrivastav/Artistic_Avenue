# Generated by Django 5.0.4 on 2024-05-02 20:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aa_app', '0013_remove_chat_artist_remove_chat_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='recipient_artist',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='received_chats', to='aa_app.artist'),
        ),
        migrations.AlterField(
            model_name='chat',
            name='recipient_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='received_chats', to='aa_app.user'),
        ),
        migrations.AlterField(
            model_name='chat',
            name='sender_artist',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sent_chats', to='aa_app.artist'),
        ),
        migrations.AlterField(
            model_name='chat',
            name='sender_type',
            field=models.CharField(choices=[('U', 'User'), ('A', 'Artist')], max_length=1),
        ),
        migrations.AlterField(
            model_name='chat',
            name='sender_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sent_chats', to='aa_app.user'),
        ),
    ]
