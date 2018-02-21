from django.http import *
from account import models as amod
from catalog import models as cmod
from django_mako_plus import view_function, jscontext


@view_function
def process_request(request):

    product = cmod.Product.objects.get(id=request.urlparams[0])
    product.status = 'I'
    product.save()
    return HttpResponseRedirect('/manager/products')


