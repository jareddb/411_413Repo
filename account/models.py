from django.db import models
from cuser.models import AbstractCUser


class User(AbstractCUser):
    # first_name
    # last_name
    # password
    # is_active
    # is_staff
    # is_superuser

    birthdate = models.DateTimeField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    zipcode = models.TextField(blank=True, null=True)

    def get_purchases(self):
        return['Roku Ultimate 2000', 'USB Cable', 'Candy Bar']


