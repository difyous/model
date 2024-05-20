import os
import re
from datetime import datetime, timedelta

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.template.defaultfilters import truncatechars
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.conf import settings
statusList  = ((0, "Enregistré"),
               (1, "Affecté"), 
               (6, "Á planifier"),
               (2, "En cours avec réserve"),
               (3, "Programmé"),
               (4, "Rejeté"),
               (5, "Accepté"))


# Structure : =================================================================================================
class Structure(models.Model):
  code = models.AutoField(primary_key=True)
  name = models.CharField(max_length=200,null=False,blank=False)
  type_structure = models.CharField(max_length=50,null=True,blank=True)
   
  def __str__(self):
    return self.name  

  class Meta:
    db_table = 'strcture'
    managed = True
    verbose_name = 'Structure'
    verbose_name_plural = 'Structures'
# User Management : =========================================================================================
class UserManager(BaseUserManager):
    def create_user(self , _username, _fullname, _email, _password=None):
        if _username is None or _username == "":
            raise TypeError("Please introduice your username.")
        if _fullname is None:
            raise TypeError("Please introduice your fullname")
        if _email is None:
            raise TypeError("Please introduice your mail")
        
          
        user = self.model(
            username=_username,
            fullname=_fullname,
            email=_email,
            is_active = True
        )
        user.set_password(_password)
        user.save(using=self._db)
        return user
    def create_superuser(self,username,password):
        if password is None:
            raise TypeError("Le mot de passe ne doit pas être vide!")
        user = self.create_user(username, "SuperUSer Account",username+"@at.dz", password)
        user.is_active = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user
class UserApp(AbstractBaseUser, PermissionsMixin):  # To add Group and permissions
    username = models.CharField(max_length=150,blank=False,unique=True,primary_key=True, verbose_name="Nom d'utilisateur")
    email   = models.EmailField(max_length=150,null=False,blank=False,unique=True, verbose_name="e-mail")
    mobile  = models.CharField(max_length=150,null=False,blank=False, verbose_name="Numéro de téléphone")

    password = models.CharField(max_length=150,blank=False,null=False, verbose_name="Mot de passe")
    fullname = models.CharField(max_length=150,null=False, verbose_name="Nom complet")
    date_joined = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_login = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    roleList  = ( (1, "Administrateur"),
                  (2, "Local"),
                  (3, "Central"))
    role      = models.SmallIntegerField(default=1,choices=roleList ,validators=[MaxValueValidator(5),MinValueValidator(1)])
    structure = models.ForeignKey(Structure, on_delete=models.SET_NULL,blank=True,null=True, related_name="Structure")
    picture   = models.ImageField(upload_to="UserApp/",null=True,blank=True)
    
    USERNAME_FIELD = "username"
    # REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        db_table = "myusers"
        managed = True
        verbose_name = "User"
        verbose_name_plural = "Users"
    
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
          }
        
    def __str__(self):
        return "{}".format(self.email)

    def get_full_name(self):
        return self.fullname

    def get_short_name(self):
        return self.username

    @property
    def is_admin(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_staff

    # def get_url(self):
    #     return "/Users/%s/?format=json" % self.username
class LogUser(models.Model):
    id = models.AutoField(primary_key=True)
    username  = models.ForeignKey(UserApp, verbose_name="Utilisateur", on_delete=models.CASCADE , related_name="+")
    dateLog   = models.DateTimeField(auto_now_add=True,verbose_name="Date d'accès")
    ipadr     = models.CharField(max_length=100,default="-",verbose_name="Addresse IP")
    def __str__(self):
        return "{} : {}".format(self.username, self.dateLog )
    class Meta:
        db_table = 'logs'
        managed = True
        verbose_name = 'Suivi des agents'
        verbose_name_plural = 'Suivi des agents'
# Custom Tables : ===========================================================================================

# Settings : ================================================================================================
class AppSettings(models.Model):
  id = models.AutoField(primary_key=True)
  theKey= models.CharField(max_length=100)
  theValue= models.CharField(max_length=100)
  
  def __str__(self):
    return self.theKey + " : " + self.theValue

  class Meta:
    db_table = 'settings'
    managed = True
    verbose_name = 'Paramètre'
    verbose_name_plural = ' Paramètres Globaux'