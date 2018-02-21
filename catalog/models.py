from django.db import models
from polymorphic.models import PolymorphicModel


class Category(models.Model):
    name = models.TextField(primary_key=True)
    create_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)


class Product(PolymorphicModel):
    """A bulk individual, or rental product"""
    TYPE_CHOICES = (
        ('BulkProduct', 'Bulk Product'),
        ('IndividualProduct', 'Individual Product'),
        ('RentalProduct', 'Rental Product'),
    )
    STATUS_CHOICES = (
        ('A', 'Active'),
        ('I', 'Inactive'),
    )

    create_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    status = models.TextField(choices=STATUS_CHOICES, default='A')
    name = models.TextField()
    description = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=7, decimal_places=2)

    def get_quantity(self):
        return 1


class BulkProduct(Product):
    """A bulk product"""
    TITLE = 'Bulk'
    quantity = models.IntegerField()
    reorder_trigger = models.IntegerField
    reorder_quantity = models.IntegerField

    def get_quantity(self):
        return self.quantity


class IndividualProduct(Product):
    """An individual product"""
    TITLE = 'Individual'
    pid = models.TextField()


class RentalProduct(Product):
    """A rental product (tracked individually"""
    TITLE = 'Rental'
    pid = models.TextField()
    max_rental_days = models.IntegerField(default=0)
    retire_date = models.DateField(null=True, blank=True)


