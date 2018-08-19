from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should be at least 2 characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "Invalid email"
        if len(User.objects.filter(email = postData['email'])) > 0:
            errors["email"] = "Contact for information on this account 555 - 6767"
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        if postData['password'] != postData['conpassword']:
            errors["conpassword"] = "Passwords must match"
        return errors
    def login_validator(self, postData):
        errors = {}
        if len(User.objects.filter(email = postData['email'])) == 0:
            errors["email"] = "Invalid Login Email"
        elif not bcrypt.checkpw(postData['password'].encode(), User.objects.get(email = postData['email']).password.encode()):
            errors["password"] = "Invalid Login Password"
        return errors

class WishManager(models.Manager):
    def wish_validator(self, postData):
        errors = {}
        if len(postData['name']) < 1:
            errors["name"] = "Wish name can't be blank (you know you wanna wish for something)"
        if len(postData['desc']) < 1:
            errors["desc"] = "Description can't be blank (you know you wanna describe something)"
        if len(postData['desc']) < 2:
            errors["desc"] = "Description should be at least 3 characters"
        if len(postData['name']) < 3:
            errors["name"] = "Wish name should be at least 3 characters"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __repr__(self):
        return "<User object: {} {} {} {}>".format(self.first_name, self.last_name, self.email, self.password)

class Wish(models.Model):
    name = models.TextField()
    desc = models.TextField()
    wisher = models.ForeignKey(User, related_name = 'wishes')
    granter = models.ForeignKey(User, related_name = 'grants',null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = WishManager()
    def __repr__(self):
        return "<Wish object: {} {} {} {}>".format(self.name, self.desc, self.wisher, self.granter)
    
class Like(models.Model):
    wish = models.ForeignKey(Wish, related_name = 'likes')
    user = models.ForeignKey(User, related_name = 'likes')
    def __repr__(self):
        return "<Like object: {} {}>".format(self.wish, self.user, self.wisher)