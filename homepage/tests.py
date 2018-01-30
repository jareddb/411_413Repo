from django.test import TestCase

# Create your tests here.

import time


localtime = time.localtime(time.time())
print(localtime.tm_year)
