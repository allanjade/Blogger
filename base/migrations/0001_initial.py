# Generated by Django 4.2.4 on 2023-08-24 03:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('user_type', models.CharField(choices=[('admin', 'Admin'), ('visitor', 'Visitor')], max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='avatar.png', upload_to='images/posts')),
                ('name', models.CharField(max_length=100)),
                ('bio', models.TextField()),
                ('telephone', models.CharField(max_length=100)),
                ('facebook', models.CharField(max_length=100, null=True)),
                ('twitter', models.CharField(max_length=100, null=True)),
                ('instagram', models.CharField(max_length=100, null=True)),
                ('youtube', models.CharField(max_length=100, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='avatar.png', upload_to='images/posts')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('created', models.DateTimeField(auto_now=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('poster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created', '-updated'],
            },
        ),
    ]
