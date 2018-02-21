from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone


@view_function
def process_request(request):
    if request.user.is_authenticated:
        loginstatus = request.user.first_name + ' ' + request.user.last_name
        hidelogin = 'none'
        hidelogout = 'block'
    else:
        loginstatus = 'Login'
        hidelogin = 'block'
        hidelogout = 'none'

    context = {
        'loginstatus': loginstatus,
        'hidelogin': hidelogin,
        'hidelogout': hidelogout,
    }
    return request.dmp_render('index.html', context)
