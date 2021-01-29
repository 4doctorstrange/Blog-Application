from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=50)
    desc = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title

class Contact(models.Model):
    name = models.CharField(null=False, max_length=50)
    email = models.EmailField()
    contact = models.CharField(max_length=12)
    message = models.TextField()
