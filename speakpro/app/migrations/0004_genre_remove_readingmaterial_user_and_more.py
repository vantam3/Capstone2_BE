# Generated by Django 5.1.1 on 2025-03-28 15:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_remove_readingmaterial_file_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='readingmaterial',
            name='user',
        ),
        migrations.RemoveField(
            model_name='speechlog',
            name='material',
        ),
        migrations.RemoveField(
            model_name='speechlog',
            name='user',
        ),
        migrations.CreateModel(
            name='SpeakingText',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('content', models.BinaryField()),
                ('language', models.CharField(blank=True, max_length=50, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='speaking_texts', to='app.genre')),
            ],
        ),
        migrations.CreateModel(
            name='Audio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('audio_file', models.BinaryField()),
                ('upload_time', models.DateTimeField(auto_now_add=True)),
                ('speaking_text', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='audio_files', to='app.speakingtext')),
            ],
        ),
        migrations.DeleteModel(
            name='Progress',
        ),
        migrations.DeleteModel(
            name='ReadingMaterial',
        ),
        migrations.DeleteModel(
            name='SpeechLog',
        ),
    ]
