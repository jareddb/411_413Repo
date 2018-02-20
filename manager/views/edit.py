from catalog import models as cmod
import re



@view_function
def process_request(request):
    cmod.Product.objects.get(id=urlparams[0])

