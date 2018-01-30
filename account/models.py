from django.db import models
from cuser.models import AbstractCUser

class User(AbstractCUser):
    birthdate = models.DateTimeField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    zipcode = models.TextField(blank=True, null=True)
    fName = models.TextField(blank=True, null=True)
    lName = models.TextField(blank=True, null=True)

    def get_purchases(self:
        return ['Roku Ultimate 2000', 'USB Cable', 'Candy Bar']




# Create your models here.
# class Question(models.Model):
#     question_text = models.TextField(blank=True, null=True)
#     question_text = models.CharField(max_length=200)
#     pub_date = models.DateTimeField('date published')
#     duration  = models.IntegerField(null=True)
#     address = models.TextField(blank=True, null=True)
#     citystatezip = models.TextField(blank=True, null=True)
