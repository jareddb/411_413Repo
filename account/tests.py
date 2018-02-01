from django.test import TestCase
from account import models as amod
from django.contrib.auth.models import Permission, Group, ContentType


class UserModelTest(TestCase):

    def test_user_create_save_load(self):
        """Tests round trip of user model data to/from database"""
        u1 = amod.User()
        u1.first_Name = 'Marge'
        u1.last_name = 'Simpson'
        u1.email = 'marge@simpsons.com'
        u1.set_password('password')
        u1.save()

        u2 = amod.User.objects.get(email='marge@simpsons.com')
        self.assertEquals(u1.first_name, u2.first_name)
        self.assertEquals(u1.last_name, u2.last_name)
        self.assertEquals(u1.email, u2.email)
        self.assertEquals(u1.password, u2.password)
        self.assertEquals(u1.check_password, u2.check_password)

    def test_add_groups_check_permissions(self):
        """Tests Permissions"""
        for p in Permission.objects.all():
            print(p.content_type.app_label + "," + p.codename)
        p1 = Permission()
        p1.name = 'Change product price'
        p1.codename = 'change_product_price'
        p1.content_type = ContentType.objects.get(id=1)
        p1.save()
        u1 = amod.User.objects.get(email='marge@simpsons.com')
        u1.user_permissions.add(p1)
        g1 = Group()
        g1.name = 'Salespeople'
        g1.permissions.add(p1)
        g1.save()
        u1.groups.add(g1)

        u1.user_permissions.add(Permission.objects.get(...))

        if u1.has_perm('change_product_price'):
            print('group creation, adding of permissions, and assigning to user successful')


    def test_create_groups(self):
        """Tests the creation of groups"""

