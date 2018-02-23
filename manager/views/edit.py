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
        new = False
    except:
        product = cmod.BulkProduct(name='', status='A', description='', category=cmod.Category(name='Brass'), price=0)
        product.TITLE = 'Bulk'
        new = True

    if request.urlparams[0] == 'submit':
        new = False

    # process the form
    form = EditForm(request, product, new)
    if form.is_valid():
        form.commit(product)
        return HttpResponseRedirect('/manager/products')

    # render the template
    return request.dmp_render('edit.html', {
      'form': form
    })


class EditForm(Formless):

    def __init__(self, request, product, new):
        self.product = product
        self.new = new
        super().__init__(request)

    #

    def init(self):
        self.fields['name'] = forms.CharField(label='Name', initial=self.product.name, required=True)
        self.fields['status'] = forms.ChoiceField(choices=self.product.STATUS_CHOICES, initial=self.product.status, required=True)

        #

        # type = None
        # if self.product.TITLE == 'Bulk':
        #     type = 'BulkProduct'
        # elif self.product.TITLE == 'Individual':
        #     type = 'IndividualProduct'
        # else:
        #     type = 'RentalProduct'

         #
        self.fields['id'] = forms.IntegerField(label=None, initial=self.product.id, required=False, widget=forms.HiddenInput())

        if self.new:
            self.fields['type'] = forms.ChoiceField(choices=cmod.Product.TYPE_CHOICES, required=False, initial=self.product.TYPE_CHOICES, widget = forms.Select(attrs={'onchange': "showFields(true);"}))
            self.fields['new'] = forms.CharField(label=None, initial='True', required=False, widget=forms.HiddenInput())
        else:
            self.fields['type'] = forms.ChoiceField(choices=cmod.Product.TYPE_CHOICES, label='Type: '+self.product.TITLE + ' Product', required=False, initial=self.product.TITLE + 'Product', widget = forms.Select(attrs={'onchange': "showFields(true);", 'style': "display:none;"}))
            self.fields['new'] = forms.CharField(label=None, initial='False', required=False, widget=forms.HiddenInput())

        print('NEWNEWNEWNEWNEW11111')
        print(self.new)

        #

        self.fields['description'] = forms.CharField(label='Description', initial=self.product.description, required=True)
        self.fields['category'] = forms.ModelChoiceField(queryset=cmod.Category.objects.all(), initial=self.product.category.name)
        self.fields['price'] = forms.DecimalField(label='Price', decimal_places=2, initial=self.product.price, required=True)

        try:
            if self.product.polymorphic_ctype.name == 'bulk product':
                prod = cmod.BulkProduct.objects.get(id=self.product.id)
                self.fields['quantity'] = forms.IntegerField(label='Quantity', initial=prod.quantity, required=False)
            else:
                self.fields['quantity'] = forms.IntegerField(label='Quantity', required=False)
        except:
            self.fields['quantity'] = forms.IntegerField(label='Quantity', required=False)

        try:
            if self.product.polymorphic_ctype.name == 'rental product':
                prod = cmod.RentalProduct.objects.get(id=self.product.id)
                self.fields['max_rental_days'] = forms.IntegerField(label='Maximum Rental Period in Days', initial=prod.max_rental_days, required=False)
                self.fields['retire_date'] = forms.DateTimeField(label='Retire Date', initial=prod.retire_date, required=False)
            else:
                self.fields['max_rental_days'] = forms.IntegerField(label='Maximum Rental Period in Days', required=False)
                self.fields['retire_date'] = forms.DateTimeField(label='Retire Date', required=False)
        except:
            self.fields['max_rental_days'] = forms.IntegerField(label='Maximum Rental Period in Days', required=False)
            self.fields['retire_date'] = forms.DateTimeField(label='Retire Date', required=False)

    #

    def clean(self):
        print('I STARTED CLEANING')
        # return the cleaned data dict, per django spec

        type_choice = self.cleaned_data.get('type')

        if type_choice == 'BulkProduct':
            if self.cleaned_data['quantity'] is None:
                raise forms.ValidationError('Please enter a quantity')

        if type_choice == 'RentalProduct':
            if self.cleaned_data['max_rental_days'] is None:
                raise forms.ValidationError('Please enter a Maximum Rental Period in Days')
            if self.cleaned_data['retire_date'] is None:
                raise forms.ValidationError('Please enter a Retire Date for the instrument')

        p1 = self.cleaned_data['price']
        if type(p1) is str:
            raise forms.ValidationError('Price must be a number')
        if p1 < 0:
            raise forms.ValidationError('Price cannot be less than 0')

        if self.cleaned_data['quantity'] is not None:
            p1 = self.cleaned_data['quantity']
            if type(p1) is not int:
                raise forms.ValidationError('Quantity must be an integer')
            if p1 < 0:
                raise forms.ValidationError('Quantity cannot be less than 0')

        if self.cleaned_data['max_rental_days'] is not None:
            p1 = self.cleaned_data['max_rental_days']
            if type(p1) is not int:
                raise forms.ValidationError('Max Rental Period in Days must be an integer')
            if p1 < 0:
                raise forms.ValidationError('Max Rental Period in Days cannot be less than 0')

        return self.cleaned_data

    #

    def commit(self, product):
        """Process the form action"""

        type_choice = self.cleaned_data.get('type')
        if self.new:
            if type_choice == 'BulkProduct':
                saveProduct = cmod.BulkProduct()
            elif type_choice == 'RentalProduct':
                saveProduct = cmod.RentalProduct()
            else:
                saveProduct = cmod.IndividualProduct()
        else:
            saveProduct = cmod.Product.objects.get(id=self.cleaned_data.get('id'))

        if type_choice == 'BulkProduct':
            saveProduct.quantity = self.cleaned_data.get('quantity')
        if type_choice == 'RentalProduct':
            saveProduct.max_rental_days = self.cleaned_data.get('max_rental_days')
            saveProduct.retire_date = self.cleaned_data.get('retire_date')

        saveProduct.name = self.cleaned_data.get('name')
        saveProduct.status = self.cleaned_data.get('status')
        saveProduct.description = self.cleaned_data.get('description')
        saveProduct.category = self.cleaned_data.get('category')
        saveProduct.price = self.cleaned_data.get('price')
        saveProduct.save()

