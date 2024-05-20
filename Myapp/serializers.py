
from django.contrib import admin,auth
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import Http404

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.relations import PrimaryKeyRelatedField

from Myapp.models import *
from django.db.models import Count, DateField, Max,Min,Avg, Q ,Sum, F
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.hashers import make_password
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
# ======================================== Models =================================================== #
class UserAppSerializer(serializers.ModelSerializer):
    date_joined = serializers.DateTimeField(format="%Y-%m-%d %H:%M",required=False)
    last_login  = serializers.DateTimeField(format="%Y-%m-%d %H:%M",required=False)
    role_name   = serializers.CharField(source='get_role_display',required=False,read_only=True) 
    
    # type_folder_name = serializers.CharField(source='get_type_folder_display',required=False,read_only=True) 
  
    class Meta:
        model = UserApp
        fields = '__all__'
    def to_representation(self, instance):
      rep = super().to_representation(instance)
      for field in rep:
        if field in rep and rep[field]:
          rep[field] = strip_tags(rep[field])
      return rep
class StructureSerializer(serializers.ModelSerializer):

  class Meta:
    model = Structure
    fields = '__all__'
  def to_representation(self, instance):
    rep = super().to_representation(instance)
    for field in rep:
      if field in rep and rep[field]:
        rep[field] = strip_tags(rep[field])
    return rep
class LogUserSerializer(serializers.ModelSerializer):
  class Meta:
    model =  LogUser
    fields = '__all__'
  def to_representation(self, instance):
    rep = super().to_representation(instance)
    for field in rep:
      if field in rep and rep[field]:
        rep[field] = strip_tags(rep[field])
    return rep
# ======================================== Custom =================================================== #