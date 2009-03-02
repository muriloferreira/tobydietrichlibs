# encoding: utf-8
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.forms import ModelForm
from registration.forms import RegistrationForm
from registration.models import RegistrationProfile

from datetime import datetime

import django.forms as forms
from django.utils.translation import ugettext_lazy as _

# I put this on all required fields, because it's easier to pick up
# on them with CSS or JavaScript if they have a class of "required"
# in the HTML. Your mileage may vary. If/when Django ticket #3515
# lands in trunk, this will no longer be necessary.
attrs_dict = { 'class': 'required' }


class EmailLoginForm(forms.Form):
    email = forms.CharField(label=_("Email"), max_length=75, widget=forms.TextInput(attrs=dict(maxlength=75)))
    password = forms.CharField(label=_(u"Password"), widget=forms.PasswordInput)

    def clean(self):
        # Try to authenticate the user
        if self.cleaned_data.get('email') and self.cleaned_data.get('password'):
            user = authenticate(username=self.cleaned_data['email'], password=self.cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    self.user = user # So the login view can access it
                else:
                    raise forms.ValidationError(_('This account is inactive. <a href="/accounts/resend_activation/">Click here</a> to resend activation email.'))
            else:
                raise forms.ValidationError(_("Please enter a correct username and password. Note that both fields are case-sensitive."))

        return self.cleaned_data

class ResendActivationForm(forms.Form):
    """
    Form for resending an activation form
    
    """
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict,
                                                               maxlength=75)),
                             label=_(u'email address'))
    def clean_email(self):
        """
        Validate that the email exists and that it has not been validated
                
        """
        try:
            user = User.objects.get(username=self.cleaned_data['email'])
        except User.DoesNotExist:
            raise forms.ValidationError(_(u'Email address not registered.'))
        try:
            registration_profile = RegistrationProfile.objects.get(user = user)
        except RegistrationProfile.DoesNotExist:
            raise forms.ValidationError(_(u'This email is already activated.'))
        if registration_profile.activation_key == RegistrationProfile.ACTIVATED:
            raise forms.ValidationError(_(u'This email is already activated.'))
        return self.cleaned_data['email']
        
        
class EmailRegistrationForm(RegistrationForm):
        def __init__(self, *args, **kwargs):
            super(EmailRegistrationForm, self).__init__(*args, **kwargs)
            del self.fields['username']
        
        def clean_email(self):
            try: 
                user = User.objects.get(username = self.cleaned_data['email'])
                raise forms.ValidationError('Email address must be unique')
            except User.DoesNotExist:
                return self.cleaned_data['email']

        def save(self, *args, **kwargs):
            # Note: if the username column has not been altered to allow 75 chars, this will not
            #       work for some long email addresses.
            self.cleaned_data['username'] = self.cleaned_data['email']
            return super(EmailRegistrationForm, self).save(*args, **kwargs)

