from django.db import models
from django.contrib.auth.models import User

class Permission(models.Model):
    name = models.CharField(max_length=225, unique=True, null=True, blank=True)
    def __str__(self):
        return self.name 
        
class Role(models.Model):
    name = models.CharField(max_length=225, unique=True, null=True, blank=True)
    permission = models.ForeignKey(Permission, null=True, on_delete=models.SET_NULL)
    def __str__(self):
        return self.name 

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,)
    role = models.ForeignKey(Role, null=True, on_delete=models.SET_NULL)
    about_me = models.TextField(blank=True)
    country = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    website = models.URLField(null=True, blank=True)
    # email = models.EmailField(max_length=254, null=True, blank=True)
    image = models.URLField(null=True, blank=True)
    date_of_birth = models.DateField(
        auto_now=False, auto_now_add=False, blank=True, null=True)
        

    def __str__(self):
        return self.user.username


class Student_data(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,)
    course_name = models.CharField(max_length=255, blank=True)
    student_roll_no = models.IntegerField(blank=True,unique=True,)
    cource_finish = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.profile.user.username