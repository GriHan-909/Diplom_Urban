from django.db import models

# Create your models here.


class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.email


class School(models.Model):
    title = models.CharField(max_length=100)
    type_of_sport = models.CharField(max_length=20)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    users = models.ManyToManyField(User)


class UserProfile(models.Model):
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField(default=0)
    email = models.EmailField()

    def __str__(self):
        return f"{self.name} {self.last_name} {self.email}"


class DateTimeTrain(models.Model):
    training_sessions = models.CharField(default='')
    date = models.DateField(null=True)
    users = models.ManyToManyField(UserProfile)
