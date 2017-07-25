from __future__ import unicode_literals
from django.db import models
import bcrypt
import datetime

class UserManager(models.Manager):
    def validateRegistration(self, form_data):
        errors = []

        if len(form_data['name']) < 3:
            errors.append("Name must be at least 3 characters")

        if len(form_data['username']) < 3:
            errors.append("Username must be at least 3 characters")


        if len(form_data['password']) < 8:
            errors.append("Password must be at least 8 characters.")

        if form_data['password'] != form_data['confirm_password']:
            errors.append("Passwords do not match")

        return errors

    def createUser(self, form_data):
        password = str(form_data['password'])
        hashed_pw = bcrypt.hashpw(password, bcrypt.gensalt())

        user = User.objects.create(
            name = form_data['name'],
            username = form_data['username'],
            password = hashed_pw
        )

        return user

    def validateLogin(self, form_data):
        errors = []

        if len(form_data['username']) == 0:
            errors.append("Username is required")

        if len(form_data['password']) == 0:
            errors.append("Password is required")

        return errors

class TripManager(models.Manager):
    def validateTrip(self, form_data):
        errors = []

        start_date = datetime.datetime.strptime(form_data['start'], '%Y-%m-%d').date()

        end_date = datetime.datetime.strptime(form_data['end'], '%Y-%m-%d').date()

        if len(form_data['destination']) == 0:
            errors.append("Trip destination is required.")
        if len(form_data['description']) == 0:
            errors.append("Trip description is required.")
        if len(form_data['start']) == 0:
            errors.append("Start date is required.")
        if len(form_data['end']) == 0:
            errors.append("End date is required.")

        if start_date < datetime.date.today():
             errors.append("Start date cannot be in the past")

        if end_date < start_date:
            errors.append("End date cannot be before start date")

        return errors

    def addTrip(self, form_data, user):
        trip = Trip.objects.create(
            destination = form_data['destination'],
            plan = form_data['description'],
            travel_start = form_data['start'],
            travel_end = form_data['end'],
            user = user
        )
        return trip


class User(models.Model):
    name = models.CharField(max_length=30)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

class Trip(models.Model):
    destination = models.CharField(max_length=30)
    travel_start = models.DateField(auto_now=False)
    travel_end = models.DateField(auto_now=False)
    plan = models.TextField(max_length=1000)
    user = models.ForeignKey(User, related_name="trips")
    travelers = models.ManyToManyField(User, related_name="travelers")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TripManager()
