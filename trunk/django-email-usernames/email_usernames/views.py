from django.conf import settings
from django.template import RequestContext
from django.contrib.auth import login
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic.list_detail import object_detail, object_list
from django.db.models import Q
from django.contrib.auth.models import User

from registration.models import RegistrationProfile
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.conf import settings

from email_usernames.forms import ResendActivationForm
from datetime import datetime


from forms import EmailLoginForm

def email_login(request, template="registration/login.html", extra_context=None):
    """A generic view that you can use instead of the default auth.login view, for email logins.
       On GET:
            will render the specified template with and pass the an empty EmailLoginForm as login_form
            with its context, that you can use for the login.
       On POST:
            will try to validate and authenticate the user, using the EmailLoginForm. Upon successful
            login, will redirect to whatever the standard LOGIN_REDIRECT_URL is set to, or the 'next'
            parameter, if specified."""

    if request.method == 'POST':
        login_form = EmailLoginForm(data=request.POST)
        if login_form.is_valid():
            # The user has been authenticated, so log in and redirect
            user = login(request, login_form.user)
            # Redirect to page pointed to by the 'next' param, or else just the first page
            next_page = request.REQUEST.get('next', settings.LOGIN_REDIRECT_URL)
            return HttpResponseRedirect(next_page)
    else:
        login_form = EmailLoginForm()

    context = { 'login_form':login_form, 'next':request.GET.get('next') }
    if extra_context is None: extra_context = {}
    for key, value in extra_context.items():
        if callable(value):
            context[key] = value()
        else:
            context[key] = value

    return render_to_response(template, context, context_instance=RequestContext(request))


def resend_activation_email(new_user, registration_profile):
    from django.core.mail import send_mail
    current_site = Site.objects.get_current()
    
    subject = render_to_string('registration/activation_email_subject.txt',
                               { 'site': current_site })
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())
    
    message = render_to_string('registration/activation_email.txt',
                               { 'activation_key': registration_profile.activation_key,
                                 'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
                                 'site': current_site })
    
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [new_user.email])
            
def resend_activation(request, template_name='registration/resend_activation.html'):
    """
    Enables user to resend activation email to him/herself.
    
    """
    if request.method == "POST":
        resend_activation_form = ResendActivationForm(data=request.POST)
        if resend_activation_form.is_valid():
            new_user = User.objects.get(username = resend_activation_form.cleaned_data['email'])
            registration_profile = RegistrationProfile.objects.get(user = new_user)
            resend_activation_email(new_user, registration_profile)
            return HttpResponseRedirect(reverse("resend_activation_complete"))
    else:
        resend_activation_form = ResendActivationForm()
    return render_to_response(template_name, {'form': resend_activation_form},
                               context_instance = RequestContext(request))

def delete_expired_users(request):
    RegistrationProfile.objects.delete_expired_users()
    return HttpResponse('{success:true}')