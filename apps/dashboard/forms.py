from django import forms
from models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
# from django.core.validators import EmailValidator
# from django.utils.translation import ugettext_lazy as _

# class EmailValid( EmailValidator ):
#     message = _('Bedite correct email')

# validate_email = EmailValid()

# class EmailField(forms.EmailField):
#     default_validators = [validate_email]

class UserForm(UserCreationForm):
    
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control input-lg'
        self.fields['email'].required = True
        # self.fields['first_name'].required = True
        # self.fields['last_name'].required = True

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class UserAutentication( AuthenticationForm ):
    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super(UserAutentication, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control input-lg'