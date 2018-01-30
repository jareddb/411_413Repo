from django.conf import settings
from django_mako_plus import view_function
from datetime import datetime
# import time

# localtime = time.localtime(time.time())
# year = localtime.tm_year

@view_function
def process_request(request):
    context = {
        'now': datetime.now(),
    }
    return request.dmp_render('index.html', context)
