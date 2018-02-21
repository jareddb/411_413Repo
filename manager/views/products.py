from django_mako_plus import view_function, jscontext
from catalog import models as cmod


@view_function
def process_request(request):
    products = list(cmod.Product.objects.filter(status='A'))
    return request.dmp_render('products.html', {'products': products})
