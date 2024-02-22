from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from ckeditor.fields import RichTextField

# Create your models here.
class Post(models.Model):
    sno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    content = RichTextField()
    author = models.CharField(max_length=20)
    slug = models.SlugField(max_length=100)
    timeStamp = models.DateTimeField(blank=True)
    views = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.title} by {self.author}'
    
class BlogComment(models.Model):
    sno = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    timeStamp = models.DateTimeField(default=now)

    def __str__(self):
        return f'{self.comment[0:20]}... by {self.user}'

