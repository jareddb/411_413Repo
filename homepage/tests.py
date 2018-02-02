from django.test import TestCase
from account import models as amod

# class UserModelTest(TestCase):
#     # def setUp(self):
#     #     Animal.objects.create(name="lion", sound="roar")
#     #     Animal.objects.create(name="cat", sound="meow")
#
#     def test_user_create_save_load(self):
#         """Tests round trip of user model data to/from database"""
#         u1 = amod.User()
#         u1.fName = 'Marge'
#         u1.lName = 'Simpson'
#         u1.email = 'marge@simpsons.com'
#         u1.set_password('password')
#         u1.save()
#
#         u2 = amod.User.objects.get(email='marge@simpsons.com')
#         self.assertEquals(u1.fName, u2.fName)
#         self.assertEquals(u1.lName, u2.lName)
#         self.assertEquals(u1.email, u2.email)
#         self.assertEquals(u1.password, u2.password)
#         self.assertEquals(u1.check_password, u2.check_password)
#
#     def test_something_else(self):
#         """Tests something else in the system"""
#
#         # """Animals that can speak are correctly identified"""
#         # lion = Animal.objects.get(name="lion")
#         # cat = Animal.objects.get(name="cat")
#         # self.assertEqual(lion.speak(), 'The lion says "roar"')
#         # self.assertEqual(cat.speak(), 'The cat says "meow"')
#
