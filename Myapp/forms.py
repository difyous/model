from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit , Field
from django.forms.widgets import HiddenInput
from Myapp.models import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class UserAppForm(forms.ModelForm):
    picture = forms.ImageField( label='Parcourir la photo de profile',
                               help_text='Seulement les fichiers images sont autorisés (JPEG, PNG, GIF).',
                               widget=forms.ClearableFileInput(attrs={'accept': '.jpg, .jpeg, .png, .gif' }))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        # self.fields['id'].required = False
        if instance and instance.pk:
            # On editing
            # self.fields["username"].widget.attrs['readonly'] = True
            # self.fields["id"].initial = instance.id
            self.fields['picture'].widget.attrs = {'class': 'form-control', 'placeholder': '','required': 'required'}
            # self.fields["confirm_Password"].widget = HiddenInput()
            
          
    def clean_picture(self):
        my_file = self.cleaned_data.get('picture')
        if my_file:
            if not my_file.content_type.startswith('image'):
                raise forms.ValidationError('Seulement les fichiers images sont autorisés.')
            # file_type = my_file.content_type.split('/')[1]
            # if file_type not in ['jpg', 'jpeg', 'png', 'pdf']:
            #     raise forms.ValidationError("Seulement les fichiers PDF, JPG, JPEG and PNG sont autorisés.")
        return my_file
    class Meta:
        model = UserApp
        # fields = "__all__"
        fields = ["picture"]

class PasswordForm(forms.ModelForm):
    password          = forms.CharField(widget = forms.PasswordInput())
    confirm_Password  = forms.CharField(widget = forms.PasswordInput())
     
    def clean(self):
      raw_password = self.cleaned_data.get('password')
      confirmPassword = self.cleaned_data.get('confirm_Password')
      if raw_password:
        if raw_password == confirmPassword :
          try:
              validate_password(raw_password)
          except ValidationError as error:
              raise forms.ValidationError(error.messages)
        else:
          raise forms.ValidationError("Les mots de passe ne correspondent pas!")
    class Meta:
        model = UserApp
        fields = ["password","confirm_Password"]
