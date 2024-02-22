from django.db import models

class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=13)
    email = models.CharField(max_length=100)
    content = models.TextField()
    timeStamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f'Message from {self.name} | {self.email}'

class Notes(models.Model):
    file_name = models.CharField(max_length=100)
    thumbnail = models.FileField(upload_to='static/img/', default=True)
    file = models.FileField(upload_to='static/pdf/')

    def __str__(self):
        return self.file_name