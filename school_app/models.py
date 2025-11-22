from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    user_type = models.CharField(max_length= 30)
class Department(models.Model):
    department_name = models.CharField(max_length=40)
    class Meta:
        db_table = 'department'

class Student(models.Model):
    department_id = models.ForeignKey(Department,on_delete=models.CASCADE)
    student_id = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.BigIntegerField()
    age = models.IntegerField()
    admission_number = models.CharField(max_length=20, null=False, blank=False)
    class Meta:
        db_table = 'student'

class Teacher(models.Model):
    department_id = models.ForeignKey(Department,on_delete=models.CASCADE)
    teacher_id = models.ForeignKey(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    phone = models.BigIntegerField()
    class Meta:
        db_table = 'teacher'