from django.test import TestCase
from account import models as amod
from django.contrib.auth.models import Permission, Group, ContentType


class UserModelTest(TestCase):

    fixtures = ['data2.yaml']

    def test_user_create_save_load(self):
        """Tests round trip of user model data to/from database"""

        self.u2 = amod.User.objects.get(email='marge@simpsons.com')

        u1 = amod.User()
        u1.first_name = 'Marge'
        u1.last_name = 'Simpson'
        u1.email = 'marge@simpsons.com'
        u1.set_password('wow')

        self.assertEquals(self.u2.first_name, u1.first_name)
        self.assertEquals(u1.last_name, self.u2.last_name)
        self.assertEquals(u1.email, self.u2.email)
        self.assertTrue(self.u2.check_password('wow'))

    def test_add_permissions(self):
        """Tests the creation and adding of Permissions"""
        self.u1 = amod.User.objects.get(email='marge@simpsons.com')

        p1 = Permission()
        p1.id = 1
        p1.name = 'Change product price'
        p1.codename = 'change_product_price'
        p1.content_type = ContentType.objects.get(id=1)
        p1.save()
        self.u1.user_permissions.add(p1)

        self.assertTrue(self.u1.has_perm('account.change_product_price'))

        # for p in Permission.objects.all():
        #     if self.u1.has_perm(p.codename):
        #         print(p.content_type.app_label + "," + p.codename)
        # print('\n')
        # if self.u1.has_perm('account.change_product_price'):
        #     print('Adding of permissions successful')

    def test_add_group_add_permissions(self):
        """tests adding a group, adding a user to that group, then adding permissions to the group and checking to see if the permissions register with the user"""
        self.u1 = amod.User.objects.get(email='marge@simpsons.com')

        g1 = Group()
        g1.name = 'Salespeople'
        g1.id = 1
        g1.save()

        # p1 = Permission()
        # p1.name = 'Change product price'
        # p1.codename = 'change_product_price'
        # p1.content_type = ContentType.objects.get(id=1)
        #
        # g1.permissions.add(p1)

        self.u1.groups.add(g1)

        self.assertGreater(self.u1.groups.filter(name='Salespeople').count(), 0)
        g1.permissions.add(Permission.objects.get(id=19))
        self.assertTrue(self.u1.has_perm('account.refund_order'))






