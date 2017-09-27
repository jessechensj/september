from __future__ import unicode_literals

from django.db import models

import datetime

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')

class UserManager(models.Manager):
    def validation(self, requestPost):
        string = ""
        if User.objects.filter(email=requestPost['email']):
            string += "| Email already exists |"
        if len(requestPost['first_name']) < 3:
            string += "| First name is too short |"
        if len(requestPost['last_name']) < 3: 
            string += "| Last name is too short |"
        if re.match(NAME_REGEX, requestPost['first_name']) == None or re.match(NAME_REGEX, requestPost['last_name']) == None:
            string += "| Name may only contain letters |"
        if re.match(EMAIL_REGEX, requestPost['email']) == None:
            string += "| Invalid E-mail |"
        if requestPost['password'] != requestPost['confirm_password']:
            string += "| Password does not match confirm password |"
        if len(requestPost['password']) < 8:
            string += "| Password too short |"
        return string

class TravelplanManager(models.Manager):
    def validation(self, requestPost):
        string = ""
        if len(requestPost['destination']) < 1:
            string += "| Destination must not be empty |"
        if len(requestPost['description']) < 1:
            string += "| Please add a description |"
        compare_time_start = datetime.datetime.strptime(requestPost['start'], '%Y-%m-%d') - datetime.datetime.today()
        print compare_time_start.total_seconds()
        if compare_time_start.total_seconds() <= 0:
            string += "| Start date has already passed |"
        compare_time_end = datetime.datetime.strptime(requestPost['end'], '%Y-%m-%d') - datetime.datetime.strptime(requestPost['start'], '%Y-%m-%d')
        if compare_time_end.total_seconds() <= 0:
            string += "| End date must be after start date |"
        return string        

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Travelplan(models.Model):
    destination = models.CharField(max_length=255)
    start = models.DateField()
    end = models.DateField()
    plan = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name = "travelplans")
    users = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TravelplanManager()