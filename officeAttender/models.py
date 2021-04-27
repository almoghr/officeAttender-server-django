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

    ON_MY_WAY = 'On my way'
    ON_MY_WAY_IN_FIVE = 'On my way in five'
    GOING_HOME = 'Going home'
    STUCK_IN_TRAFFIC = 'Stuck in traffic'
    AT_THE_OFFICE = 'At the office'
    SICK_AT_HOME = 'Sick at home'
    IN_A_MEETING = 'In a meeting'
    IN_A_STAFF_MEETING = 'In a staff meeting'
    IN_A_MANAGEMENT_MEETING = 'In a management meeting'
    COFFEE_BREAK = 'Coffee break'
    LUNCH_TIME = 'Lunch time'
    IN_A_PARALLEL_WORKSPACE = 'In a parallel workspace'
    WORKING_FROM_HOME = 'Working from home'

    WHATS_MY_STATUS = [
        (ON_MY_WAY, 'On my way'),
        (ON_MY_WAY_IN_FIVE, 'On my way in five'),
        (GOING_HOME, 'Going home'),
        (STUCK_IN_TRAFFIC, 'Stuck in traffic'),
        (AT_THE_OFFICE, 'At the office'),
        (SICK_AT_HOME, 'Sick at home'),
        (IN_A_MEETING, 'In a meeting'),
        (IN_A_STAFF_MEETING, 'In a staff meeting'),
        (IN_A_MANAGEMENT_MEETING, 'In a management meeting'),
        (COFFEE_BREAK, 'Coffee break'),
        (LUNCH_TIME, 'Lunch time'),
        (IN_A_PARALLEL_WORKSPACE, 'In a parallel workspace'),
        (WORKING_FROM_HOME, 'Working from home'),
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
