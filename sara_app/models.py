from django.db import models

# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


def user_directory_path(instance, filename):
    name, ext = filename.split(".")
    name = instance.name
    filename = name +'.'+ ext
    return 'Faculty_Images/'+name+'/{}'.format(filename)

class Employees(models.Model):
    empid = models.IntegerField()
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=10)
    profilepic = models.ImageField(upload_to=user_directory_path)

    def __str__(self):
        return self.name

class Attendance(models.Model):
    # empid = models.IntegerField()
    name = models.CharField(max_length=100)
    punchin = models.CharField(max_length=100)
    punchout = models.CharField(max_length=100)

    def __str__(self):
        return self.name
