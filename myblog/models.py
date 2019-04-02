from django.db import models

# Create your models here.


class UserInfo(models.Model):
    username = models.CharField(max_length=64)
    sex = models.CharField(max_length=64)
    email = models.CharField(max_length=64)

class Article(models.Model):
    title = models.CharField(max_length=64, default="Title")
    content = models.TextField(null=True)

class Classes(models.Model):
    caption = models.CharField(max_length=32)

class Student(models.Model):
    name = models.CharField(max_length=32)
    cls = models.ForeignKey('Classes', on_delete=models.CASCADE)

class Teacher(models.Model):
    name = models.CharField(max_length=32)
    cls = models.ManyToManyField('Classes')







