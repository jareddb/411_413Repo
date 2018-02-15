from django.db import models


class Category():
    create_date = models.DateTimeField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
