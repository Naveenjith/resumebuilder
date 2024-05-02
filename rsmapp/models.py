from django.db import models
from django.contrib.auth.models import User

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    dob = models.DateField()
    email = models.EmailField()
    address = models.TextField()
    profile = models.TextField()
    skills = models.TextField()
    education = models.TextField()
    experience = models.TextField()
    image = models.ImageField(upload_to='resume_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.fname} {self.lname}'s Resume"
