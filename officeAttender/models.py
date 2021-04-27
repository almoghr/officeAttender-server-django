from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(('email address'))

    
class WorkSpace(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description =models.TextField(max_length=350)
    address = models.CharField(max_length=50)

    def __str__(self):
        return self.name



class Employee(models.Model):


    WHATS_MY_STATUS = [
        ('On my way', 'On my way'),
        ('On my way in five', 'On my way in five'),
        ('Going home', 'Going home'),
        ('Stuck in traffic', 'Stuck in traffic'),
        ('At the office', 'At the office'),
        ('Sick at home', 'Sick at home'),
        ('In a meeting', 'In a meeting'),
        ('In a staff meeting', 'In a staff meeting'),
        ('In a management meeting', 'In a management meeting'),
        ('Coffee break', 'Coffee break'),
        ('Lunch time', 'Lunch time'),
        ('In a parallel workspace', 'In a parallel workspace'),
        ('Working from home', 'Working from home'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    occupation = models.CharField(max_length=50)
    occupationDescription = models.TextField(max_length=350)
    is_management = models.BooleanField(blank=True, default=False)
    status = models.CharField(max_length=50, choices=WHATS_MY_STATUS, default=None, blank=True, null=True)
    lastUpdated = models.DateField(auto_now_add=True)
    address = models.CharField(max_length=250)
    workspace = models.ForeignKey(WorkSpace, on_delete=models.CASCADE) 

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        self.user.delete()
        return super(self.__class__, self).delete(*args, **kwargs)



# Create your models here.
