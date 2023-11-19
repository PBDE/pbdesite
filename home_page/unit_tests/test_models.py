from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

from .test_views import create_user_data

class CustomUserModelTest(TestCase):
    
    def test_duplicate_email_addresses_not_allowed(self):

        user_data1 = create_user_data()
        user_data2 = create_user_data()
        get_user_model().objects.create_user(user_data1["username"], user_data1["email"], user_data1["password1"])
        with self.assertRaises(IntegrityError):
            get_user_model().objects.create_user(user_data2["username"], user_data1["email"], user_data2["password1"])
