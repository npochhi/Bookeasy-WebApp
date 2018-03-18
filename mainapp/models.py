from django.db import models

# Create your models here.

class UserProfile(models.Model):
    email = models.EmailField(primary_key = True)
    password = models.CharField(max_length = 30, unique = True)
    authenticated = models.BooleanField(default = False)
    
class Student(models.Model):
    ID = models.CharField(max_length = 20, unique = True)
    email = models.EmailField(primary_key = True)
    name = models.CharField(max_length = 30)
    mobile_no = models.CharField(max_length = 10)

class Employee(models.Model):
    designation_choices = (
        ('ASSP', 'Assistant Professor'),
        ('ASOP', 'Associate Professor'),
        ('PROF', 'Professor'),
        ('LABT', 'Lab Technician'),
        ('ACCO', 'Accountant'),
        ('PROJ', 'Project Officer'),
    )

    ID = models.CharField(max_length = 20, unique = True)
    email = models.EmailField(primary_key = True)
    name = models.CharField(max_length = 30)
    mobile_no = models.CharField(max_length = 10)
    designation = models.CharField(max_length = 4, choices = designation_choices, default = 'ASSP')

class ApprovalEntity(models.Model):
    category_choices = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    )

    user_ID = models.ForeignKey(UserProfile, on_delete = models.CASCADE)
    approval_ID = models.ForeignKey(Employee, on_delete = models.CASCADE)
    category = models.CharField(max_length = 1, choices = category_choices)

    class Meta:
        unique_together = ('user_ID', 'approval_ID', 'category')