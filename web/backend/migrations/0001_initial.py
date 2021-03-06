# Generated by Django 3.0.8 on 2020-07-09 11:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pic_name', models.CharField(max_length=32)),
                ('pic_img', models.ImageField(upload_to='images')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=32)),
                ('title', models.CharField(max_length=32)),
                ('content', models.CharField(max_length=512)),
                ('add_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('name', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('content', models.CharField(max_length=256)),
                ('add_time', models.DateTimeField(auto_now_add=True)),
                ('answer_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.Post')),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_name', models.CharField(max_length=64)),
                ('add_time', models.DateTimeField(auto_now_add=True)),
                ('download', models.IntegerField(default=0)),
                ('book_state', models.IntegerField(default=1)),
                ('title', models.CharField(default='', max_length=64)),
                ('intro', models.CharField(default='', max_length=256)),
                ('is_upload', models.IntegerField(default=0)),
                ('user_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.User')),
            ],
        ),
    ]
