from django.db import models

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager


# Create your models here.
class UserProfileManager(BaseUserManager):
    """ Helps django to work with custom user """
    def create_user(self, email, name, password = None):
        """ Creates a new user object """
        if not email:
            raise ValueError('User most have an email address.')
        email = self.normalize_email(email)
        user = self.model(email = email, name = name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        """ Creates and saves a new super user """
        user = self.create_user(email, name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user



class UserProfile(AbstractBaseUser, PermissionsMixin):
    """ Represent a user profile inside our system """
    email = models.EmailField(max_length = 255, unique = True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)

    objects = UserProfileManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """ Use to get the user full name """

        return self.name
    
    def get_short_name(self):
        """ Get the short name of the user """
        return self.name
    
    def __str__(self):
        """ Convert object to string """
        return self.email


class ProfileFeedItem(models.Model):
    """ profile status update """
    user_profile = models.ForeignKey("UserProfile", on_delete=models.CASCADE)
    status_text = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    contributors = models.ManyToManyField("Contributor")
    def __str__(self):
        """ Return the model as a string """
        return self.status_text
    
class Contributor(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    def __str__(self):
        return self.name
    
