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
    form = SignupForm(request)
    if form.is_valid():
        form.commit()
        return HttpResponseRedirect('/account/index')

    # render the template
    return request.dmp_render('signup.html', {
      'form': form
    })


class SignupForm(Formless):

    def __init__(self, request):
        super().__init__(request)
        self.user = None
        self.email = None
        self.p1 = None
        self.p2 = None

    def init(self):
        """Adds the fields for this form"""
        # self.fields['first_name'] = forms.CharField(label='First Name')
        # self.fields['last_name'] = forms.CharField(label='Last Name')
        # self.fields['birthdate'] = forms.CharField(label='Birth Date')
        # self.fields['address1'] = forms.CharField(label='Address Line 1')
        # self.fields['address2'] = forms.CharField(label='Address Line 2')
        # self.fields['city'] = forms.CharField(label='City')
        # self.fields['state'] = forms.CharField(label='State')
        # self.fields['zip'] = forms.CharField(label='Zipcode')
        self.fields['email'] = forms.CharField(label='Email Address')
        self.fields['password'] = forms.CharField(label='Password', widget=forms.PasswordInput())
        self.fields['password2'] = forms.CharField(label='Confirm Password', widget=forms.PasswordInput())

    #

    def clean(self):
        p2 = self.cleaned_data['password2']
        print(self.p1)
        if self.p1 != p2:
            raise forms.ValidationError('Passwords do not match')

        # return the cleaned data dict, per django spec
        return self.cleaned_data

    #

    def clean_email(self):
        print(self.cleaned_data)
        self.email = email = self.cleaned_data['email']

        if amod.User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists in the database')
        return self.cleaned_data
    #

    def clean_password(self):
        self.p1 = p1 = self.cleaned_data['password']
        if len(p1) < 8:
            raise forms.ValidationError('Password must be at least 8 characters long')

        if re.search('[0-9]', p1) is None:
            raise forms.ValidationError('Password must contain a number')

    #

    def commit(self):
        """Process the form action"""
        user = amod.User.objects.create_user(self.email, password=self.p1)
        user.save()
        login(self.request, user)



