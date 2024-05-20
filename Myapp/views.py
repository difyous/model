import json, sys, os
import math, base64, re
import time as functiontimer
from PIL import Image
from io import BytesIO
from os import mkdir, path, getcwd
from uuid import uuid4

from django.shortcuts import get_object_or_404, redirect, render
from django.conf import settings
from django.db import connection
from django.db.models import Count, DateField, Max,Min,Avg, Q ,Sum, F
from django.db.models.functions.datetime import ExtractMonth, TruncDate, TruncMonth
from django.forms.models import model_to_dict
from django.contrib.auth import authenticate, login, logout , update_session_auth_hash , get_user_model , REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.contrib.sitemaps import Sitemap
from django.core.serializers.json import DjangoJSONEncoder
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.serializers import serialize
from django.urls import reverse
from django.http import JsonResponse, Http404, HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.http.response import HttpResponseServerError

from django.template import TemplateDoesNotExist
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page,cache_control
from django_filters import rest_framework as filters

from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import generics, status, views,viewsets
from rest_framework.permissions import IsAuthenticated

from itertools import chain, groupby
from datetime import datetime, timedelta
from Myapp.models import *
from Myapp.serializers import  *
from Myapp.forms import  *
from django.template import loader
from django import template
from django.contrib import messages, auth

# File Management===============================================
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
import csv
# JWT ==========================================================
import jwt
from .utils import Util
from drf_yasg import openapi
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import permissions
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema

from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.http import HttpResponseRedirect

from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password

from django.utils.http import url_has_allowed_host_and_scheme
from axes.decorators import axes_dispatch 
from axes.models import AccessAttempt
from django.utils.html import strip_tags
from rest_framework_simplejwt.backends import TokenBackend

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.template import loader

from django.views.decorators.http import require_http_methods


# Common functions ===============================-------------------------------========================================
class SuccessURLAllowedHostsMixin:
    success_url_allowed_hosts = set()

    def get_success_url_allowed_hosts(self):
        return {self.request.get_host(), *self.success_url_allowed_hosts}
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
def date_in_range(start, end, current):
    """Returns whether current is in the range [start, end]"""
    return start <= current <= end

def validate_file_size(value):
  if value.size > 50 * 1024 * 1024:  # 10 MB
      return False
  return True
def validate_file_extension(value):
  file_extension = value.name.split('.')[-1].lower()
  if file_extension not in settings.VALID_EXTENSION:
      return False
  return True

  
# APIs ==========================================-------------------------------========================================
# API ViewSets :--------------------------------------------------------------------------------------------------------
minDat_inp= openapi.Parameter('minDate',in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description="MinDate",example= "2022-01-01",default= "2022-01-01",)
maxDat_inp= openapi.Parameter('maxDate',in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description="MaxDate",example= "2023-01-01",default= "2023-01-01",)
client_inp= openapi.Parameter('Client',in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description="Client",example= "client1",default= "",)
status_inp= openapi.Parameter('Status',in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description="Status",example= 0,default= 0,)
type_inp= openapi.Parameter('Type',in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description="Status 0 | 1 | 2 ",example= 0,default= 0,)
# JWT ==============================================-------------------------------========================================
# ModelViewSet =====================================-------------------------------========================================
class UserViewSet(viewsets.ModelViewSet):
    queryset = UserApp.objects.all()
    serializer_class = UserAppSerializer
    permission_classes = (IsAuthenticated, )
    http_method_names = ['get','post','patch','delete','head','option']
class StructureViewSet(viewsets.ModelViewSet):
  permission_classes = (IsAuthenticated, )
  queryset = Structure.objects.all()
  serializer_class = StructureSerializer
class ATUserViewSet(viewsets.ModelViewSet):
  permission_classes = (IsAuthenticated, )
  queryset = UserApp.objects.all()
  serializer_class = UserAppSerializer
# GenericAPIView =====================================-------------------------------========================================
class LoginAPI(generics.GenericAPIView):
    http_method_names = ['post']
    def post(self, request):
        try:
            username    = self.request.data['username']
            userItem = authenticate(request=request, username=user_data['username'], password=request.data['password'], backend='django.contrib.auth.backends.ModelBackend')
             
            response = {    "Status": 1,
                            "username": userItem.username,
                            "fullName": userItem.fullName,
                            "active"  : userItem.is_active,
                            }
            # Save a log about it:
            LogUser(username=userItem, ipadr=get_client_ip(request)).save()
            request.session['Adm_username'] = userItem.username
            request.session['Adm_password'] = self.request.data['password']
            request.session['Adm_fullname'] = userItem.fullName
           
            return JsonResponse(response)            
        except KeyError as e:
            print("KeyError : ",e)
            response = {     'Status' : 0 , 
                            'Message': " Erreur dans l\'input >> " + str(e)
                        }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("Exception : ",e)
            response = {     'Status' : 0 , 
                            'Message': str(e)
                        }
            return Response(response,status=status.HTTP_200_OK) 
# Common Pages ==============================-------------------------------========================================
@require_http_methods(["POST"])
def login_post(request):
    user_data = request.POST
    userItem = authenticate(request=request, username=user_data['username'], password=user_data['password'], backend='django.contrib.auth.backends.ModelBackend')       
    if userItem is not None and user_data['password'] == settings.DEFAULT_PASSWORD[0]:
        myContext = {
            "user": user_data['username'],
        }
        return render(request, 'password.html', myContext)
    
    if userItem is not None:
        login(request, userItem, backend='django.contrib.auth.backends.ModelBackend')
        LogUser(username=userItem, ipadr=get_client_ip(request)).save()
        
        if 'next' in request.POST and url_has_allowed_host_and_scheme(request.POST['next'], allowed_hosts=None):
            return redirect(request.POST['next'])
        else:
            return redirect(reverse("index"))
    else:
        messages.error(request, "Prière de vérifier vos coordonnées")
        return render(request, 'login.html')

@axes_dispatch
@require_http_methods(["GET"])
def LoginPage(request):
    template_url = "login.html"
    if not request.user.is_anonymous:
        return redirect(reverse("index"))
    return render(request, template_url)

@require_http_methods(["POST"])
def PasswordReset(request):
    user_data = request.POST
    userItem = get_object_or_404(UserApp , username = user_data["user"]) 
    userItem.set_password(user_data["newPassword"])
    userItem.save()
    messages.success(request, "Mot de passe changé avec succès!")
    
    return redirect("/login/")
@require_http_methods(["GET"]) 
def LogoutPage(request):
    auth.logout(request)
    # messages.success(request, 'Merci pour votre visite!')
    return redirect('login')
@require_http_methods(["GET"])
def user_lockout(request, credentials):
    """
    Custom accout lockout message for django-axes.
    change custom_account_lockout_message accordingly to what you need.
    """
    ip_address = get_client_ip(request)
    # Get the most recent access attempt for the user and IP address
    attempt = AccessAttempt.objects.filter(ip_address=ip_address).latest('attempt_time')
    dt = abs(timezone.now()  - attempt.attempt_time)
    # Calculate the remaining time until the user can attempt to log in again
    response_data = {
        "login": "Failed",
        "error": settings.CUSTOM_AXES_SOFT_LOCKOUT_MESSAGE,
        "CoolTime": settings.AXES_COOLOFF_TIME.seconds -  dt.seconds,
    }
    return render(request, 'lockout.html',response_data)
    # return HttpResponse(JsonResponse(response_data))
@require_http_methods(["GET"])
def Errorhandler404(request, exception):
    myContext ={
      "exception" : "//{}{}".format(request.get_host() , request.path),
      }
    return render(request, '404.html', myContext, status=404)
@require_http_methods(["POST"])
def Errorhandler403(request,reason=""):
    myContext ={
      "exception" : "403: " + str(reason),
      }
    return render(request, '500.html', myContext, status=403)
@require_http_methods(["GET"])
def Errorhandler500(request,):
    exception_type, exception_object, exception_traceback = sys.exc_info()
    filename = exception_traceback.tb_frame.f_code.co_filename
    line_number = exception_traceback.tb_lineno
    myContext ={ "exception" : exception_object, }
    t = loader.get_template('500.html')
    type, value, tb = sys.exc_info()
    return HttpResponseServerError(t.render(myContext,request))
# Custom Pages ==============================-------------------------------========================================
@login_required(login_url="/login/")
@require_http_methods(["GET"])
def IndexPage(request):
    redirecturl = "login"
    
    if request.user.username is not None :
        try:
          userItem    = UserApp.objects.get(username=request.user.username)
        except:
          return redirect("/logout/")
        if userItem.role == 1: redirecturl = "profil"
        if userItem.role == 2: redirecturl = "admin"
        if userItem.role == 3: redirecturl = "admin"
        if userItem.role == 4: redirecturl = "admin"
    return redirect(reverse(redirecturl))

@require_http_methods(["POST"])
def post_profil_page(request):
    theUser = get_object_or_404(UserApp, username=request.user.username)
    if "password" in request.POST:
        form = PasswordForm(request.POST, instance=theUser)
        if form.is_valid():
            instance = form.save(commit=False)
            hashed_password = make_password(request.POST["password"])
            instance.password = hashed_password
            instance.save()
            messages.success(request, "Mot de passe modifié avec succès.")
        else:
            messages.error(request,str(form.errors).replace("__all__","Mot de passe"))
    else:
        form = UserAppForm(request.POST, request.FILES, instance=theUser)
        if form.is_valid():
            if request.FILES:
                instancePic = form.save(commit=False)
                instancePic.save()
                messages.success(request, "Photo de profil modifiée avec succès.")
        else:
            messages.error(request,form.errors)
    return HttpResponseRedirect(reverse("profil"))
@login_required(login_url="/login/")
@require_http_methods(["GET"])
def ProfilPage(request):
  theUser = get_object_or_404(UserApp, username=request.user.username)
  form = PasswordForm(instance=theUser)
  formPicture = UserAppForm(instance=theUser)
  myContext = {
      "MenuUser": "active",
      "form": form,
      "formPicture": formPicture,
      "theUser": theUser,
  }
  return render(request, 'user.html', myContext)
# Form submitting ===============================---------------------==============================================
