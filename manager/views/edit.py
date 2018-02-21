from catalog import models as cmod
from django import forms
from django.http import *
from account import models as amod
from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from formlib import Formless
import re


@view_function
def process_request(request):
    try:
        product = cmod.Product.objects.get(id=request.urlparams[0])
    except:
        product = cmod.Product(name='', status='A', description='', category=cmod.Category(name='Brass'), price=0)

    # process the form
    form = EditForm(request, product)
    print('I FINISHED RENDERING THE FORM')
    if form.is_valid():
        print('THE FORM IS VALID')
        form.commit()
        return HttpResponseRedirect('/manager/products')

    # render the template
    return request.dmp_render('edit.html', {
      'form': form
    })


class EditForm(Formless):

    def __init__(self, request, product):
        self.product = product
        super().__init__(request)

    def init(self):
        self.fields['name'] = forms.CharField(label='Name', initial=self.product.name)
        self.fields['status'] = forms.ChoiceField(choices=self.product.STATUS_CHOICES, initial=self.product.status)
        self.fields['TYPE_CHOICES'] = forms.ChoiceField(choices=self.product.TYPE_CHOICES, widget = forms.Select(attrs = {'onchange' : "showFields(true);",}))
        self.fields['description'] = forms.CharField(label='Description', initial=self.product.description)
        self.fields['category'] = forms.ChoiceField(choices=[[x.name, x.name] for x in cmod.Category.objects.all()], initial=self.product.category.name)
        # self.fields['category2'] = forms.ModelChoiceField(queryset=cmod.Category.objects.all())
        self.fields['price'] = forms.DecimalField(label='Price', decimal_places=2, initial=self.product.price)

        try:
            if self.product.polymorphic_ctype.name == 'bulk product':
                prod = cmod.BulkProduct.objects.get(id=self.product.id)
                self.fields['quantity'] = forms.IntegerField(label='Quantity', initial=prod.quantity)
            else:
                self.fields['quantity'] = forms.IntegerField(label='Quantity')
        except:
            self.fields['quantity'] = forms.IntegerField(label='Quantity')

        try:
            if self.product.polymorphic_ctype.name == 'rental product':
                prod = cmod.RentalProduct.objects.get(id=self.product.id)
                self.fields['max_rental_days'] = forms.IntegerField(label='Maximum Rental Period in Days', initial=prod.max_rental_days)
                self.fields['retire_date'] = forms.DateTimeField(initial=prod.retire_date)
            else:
                self.fields['max_rental_days'] = forms.IntegerField(label='Maximum Rental Period in Days')
                self.fields['retire_date'] = forms.DateTimeField()
        except:
            self.fields['max_rental_days'] = forms.IntegerField(label='Maximum Rental Period in Days')
            self.fields['retire_date'] = forms.DateTimeField()

    def clean(self):
        print('I STARTED CLEANING')
        # self.product = self.product
        #
        # if self.product is None:
        #     raise forms.ValidationError('You should not be capable of committing this error')

        # return the cleaned data dict, per django spec
        return self.cleaned_data

    def commit(self):
        """Process the form action"""
        if self.product.polymorphic_ctype.name == 'bulk product':
            self.product.quantity = self.cleaned_data.get('quantity')

        if self.product.polymorphic_ctype.name == 'rental product':
            self.product.max_rental_days = self.cleaned_data.get('max_rental_days')
            self.product.retire_date = self.cleaned_data.get('retire_date')

        self.product.name = self.cleaned_data.get('name')
        self.product.status = self.cleaned_data.get('status')
        self.product.TYPE_CHOICES = self.cleaned_data.get('TYPE_CHOICES')
        self.product.description = self.cleaned_data.get('description')
        self.product.category = self.cleaned_data.get('category')
        self.product.price = self.cleaned_data.get('price')

        self.product.save()

