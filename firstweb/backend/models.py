from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Book(models.Model):
    book_name = models.CharField(max_length=64)
    user_name = models.ForeignKey('User', on_delete=models.CASCADE, to_field='name')
    add_time = models.DateTimeField(auto_now_add=True)
    download = models.IntegerField(default=0)
    book_state = models.IntegerField(default=1)
    title = models.CharField(max_length=64, default='')
    intro = models.CharField(max_length=256, default='')
    is_upload = models.IntegerField(default=0)

    def __unicode__(self):
        return self.book_name


class User(models.Model):
    name = models.CharField(max_length=32, primary_key=True)
    password = models.CharField(max_length=32)

    def __unicode__(self):
        return self.name


class Pic(models.Model):
    pic_name = models.CharField(max_length=32)
    pic_img = models.ImageField(upload_to='images')

    def __unicode__(self):
        return self.pic_name


class Post(models.Model):
    user_name = models.CharField(max_length=32)
    title = models.CharField(max_length=32)
    content = models.CharField(max_length=512)
    add_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.user_name


class Comment(models.Model):
    name = models.CharField(max_length=32)
    answer_post = models.ForeignKey('Post', on_delete=models.CASCADE, to_field='id')
    content = models.CharField(max_length=256)
    add_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name
