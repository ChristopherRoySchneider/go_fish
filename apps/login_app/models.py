from __future__ import unicode_literals
from django.db import models
from datetime import datetime
import re
import bcrypt
# from dateutil.relativedelta import relativedelta

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validate_login(self,postData):
        print("in validate_login")
        errors = {}
        
        
        try:
            print("in validate_login 1")
            user = User.objects.get(email=postData['email'])
            if bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                errors = {}
                return errors
            else:
                errors["login"] = "Login failed"
                return errors
        except:
            print("in validate_login 2")
            errors["login"] = "Login failed"
            return errors
        
        
        
  
                
    def basic_validator(self, postData):
        errors = {}
        try:
            email_check = User.objects.exclude(id = postData['user_id']).filter(email = postData['email']).count()
            
            
        except:
            email_check = User.objects.filter(email = postData['email']).count()
            

        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should be at least 2 characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors["email_format"] = "Email format incorrect"
        elif email_check:
            errors["email_unique"] = "Email address already registered"
        if postData['password']!=postData['confirm_password']:
            errors["pw_match"] = "Passwords must match"
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        if postData['birthday']=="":
            errors["birthday_missing"] = "Enter your birthday"
        else:
            dt = datetime.now()
            if datetime.strptime(postData['birthday'],"%Y-%m-%d") > dt:
                errors["birthday"] = "Birthday must be in the past"
            elif datetime.strptime(postData['birthday'],"%Y-%m-%d") > dt.replace(year = dt.year-1):
                errors["birthday_too_young"] = "Minimum user age is 1 years old"
        
       
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birthday = models.DateField()
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

