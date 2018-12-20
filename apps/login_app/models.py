from __future__ import unicode_literals
from django.db import models
import bcrypt

class UserManager(models.Manager):
    def validate_login(self,postData):
        errors = {}
        try:
            user = User.objects.get(username=postData['username'])
            if bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                errors = {}
                return errors
            else:
                errors['login'] = 'Login failed.'
                return errors
        except:
            errors['login'] = 'Login failed.'
            return errors
                
    def basic_validator(self, postData):
        errors = {}
        try:
            username_in_use = User.objects.exclude(id = postData['user_id']).filter(username = postData['username']).count()
        except:
            username_in_use = User.objects.filter(username = postData['username']).count()
        if username_in_use:
            errors['username_unique'] = 'Username already in use. Please log in.'
        if len(postData['first-name']) < 2:
            errors['first-name'] = 'First name should be at least 2 letters.'
            return errors
        if len(postData['last-name']) < 2:
            errors['last-name'] = 'Last name should be at least 2 letters.'
            return errors
        if len(postData['username']) < 2:
            errors['username'] = 'Username should be at least 2 characters.'
            return errors
        if postData['password']!=postData['confirm_password']:
            errors['pw_match'] = 'Passwords do not match.'
            return errors
        if len(postData['password']) < 8:
            errors['password'] = 'Password should be at least 8 characters.'
            return errors
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()