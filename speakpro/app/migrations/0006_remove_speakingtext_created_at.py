# Generated by Django 5.1.1 on 2025-03-29 09:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_speakingtext_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='speakingtext',
            name='created_at',
        ),
    ]
