import os
from pprint import pprint

from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.db.models import Avg, Count, DateField, F, Max, Min, Q, Sum
from django.utils.html import format_html
from django.contrib import messages
from django.utils.safestring import mark_safe
from Myapp.models import *
from import_export import resources, widgets
from import_export.admin import ExportActionMixin, ImportMixin ,ImportExportModelAdmin
from import_export.fields import Field
@admin.action(description='Dupliquer la sélection')   
def duplicate_AutoID(modeladmin, request, queryset):
    for object in queryset:
      object.id = None
      object.save()
duplicate_AutoID.short_description = "Duplicate selected record"
# User Admin ============================================================================================
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        help_text= ("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using  this button <input type='button' class='btn btn-sm btn-outline-danger' onclick='location.href=\"../password/\";'value='Change Password' />"))

    class Meta:
        model = UserApp
        fields = '__all__'

    def clean_password(self):
        return self.initial["password"]
@admin.register(UserApp)
class UserAdmin(BaseUserAdmin):
    def image_tag(self, obj):
        try:
          return format_html('<img src="{}"  class="img img-circle img-thumbnails"  width="75px" height="75px" />'.format(obj.picture.url))
        except:
          return format_html('<img src="/assets/images/users/user-dummy-img.jpg" class="img img-circle img-thumbnails" width="75px" height="75px" />')
    form = UserChangeForm
    list_display =  ('username','fullname','image_tag' ,'role', 'is_active', 'is_staff', 'is_superuser')
    
    # lookup_field = 'id'
    fieldsets = (
        ('Information Commune', {'fields': ( 'role', 'username','password')}),
        ('Information personnelle', {'fields': ('fullname', 'email', 'mobile', 'picture','image_tag')}),
        ('Permissions', {'fields': ('is_active','is_staff','is_superuser')}),
    )
    # readonly_fields =('last_login',)
    search_fields = ('username', 'fullname')
    ordering = ('fullname',)
    list_display_links = ["username","fullname",]
    list_editable = ["is_active","role"]
    readonly_fields = ("date_joined","last_login","image_tag")
    list_filter = ('is_staff','role','structure','is_active','is_superuser')
    
    actions = [duplicate_AutoID]

@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    # to have a date-based drilldown navigation in the admin page
    date_hierarchy = 'action_time'
    # to filter the resultes by users, content types and action flags
    list_filter = [ 'user', 'content_type', 'action_flag']
    # when searching the user will be able to search in both object_repr and change_message
    search_fields = [ 'object_repr','change_message']
    list_display = [ 'action_time', 'user', 'content_type', 'action_flag', ]    
 
# class Tab_Files(admin.TabularInline):
#     model = DossierFile 
@admin.register(LogUser)
class LogUserAdmin(admin.ModelAdmin):
    list_display= [field.name for field in LogUser._meta.get_fields()]
    #    inlines = [Tab_Files,Tab_Calendar]

class StructureResource(resources.ModelResource):
    class Meta:
        model = Structure
        fields = ("code","name","type_structure")
        import_id_fields = ['code',]

@admin.register(Structure)
# class StructureAdmin(ImportMixin, ExportActionMixin, admin.ModelAdmin):
class StructureAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display= ["code","name","type_structure"]
    resource_class = StructureResource

# admin.site.unregister(Group)
# Custom ======================================================================================================
@admin.register(AppSettings)
class AppSettingsAdmin(ImportExportModelAdmin):
    list_display= [field.name for field in AppSettings._meta.get_fields()]