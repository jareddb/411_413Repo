from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django_mako_plus import view_function
from formlib import Formless
from django import forms
from account import models as amod
import re

@view_function
def process_request(request):

    # process the form
    form = LoginForm(request)
    if form.is_valid():
        form.commit()
        return HttpResponseRedirect('/homepage/index')

    # render the template
    return request.dmp_render('login.html', {
      'form': form
    })


class LoginForm(Formless):

    def __init__(self, request):
        super().__init__(request)
        self.user = None
        self.email = None
        self.p = None

    def init(self):
        """Adds the fields for this form"""
        self.fields['email'] = forms.CharField(label='Email Address')
        self.fields['password'] = forms.CharField(label='Password', widget=forms.PasswordInput())

    def clean(self):
        self.user = authenticate(email=self.cleaned_data.get('email'), password=self.cleaned_data.get('password'))

        if self.user is None:
            raise forms.ValidationError('Invalid email or password.')

        # return the cleaned data dict, per django spec
        return self.cleaned_data

    def commit(self):
        """Process the form action"""
        login(self.request, self.user)




