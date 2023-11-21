from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from home_page.forms import CustomUserCreationForm, LoginForm
from portfolio.functional_tests.base import FunctionalTest

from home_page.views import INDEX_TEMPLATE, REGISTER_TEMPLATE, LOGIN_TEMPLATE, ACCOUNT_TEMPLATE, DELETE_ACCOUNT_TEMPLATE

def create_user_data():
    functional_test = FunctionalTest()
    username = functional_test.random_user_details(functional_test.UserDetails.USERNAME)
    password = functional_test.random_user_details(functional_test.UserDetails.PASSWORD)
    email = functional_test.random_user_details(functional_test.UserDetails.EMAIL)
    user_data = {"username": username, 
            "password1": password, 
            "password2": password, 
            "email": email}
    return user_data

class IndexViewTest(TestCase):

    def test_index_template_returned(self):
        response = self.client.get(reverse("home_page:index"))
        self.assertTemplateUsed(response, INDEX_TEMPLATE)


class RegisterViewTest(TestCase):

    def test_register_template_returned(self):
        response = self.client.get(reverse("home_page:register"))
        self.assertTemplateUsed(response, REGISTER_TEMPLATE)

    def test_register_form_returned(self):
        response = self.client.get(reverse("home_page:register"))
        self.assertIsInstance(response.context["form"], CustomUserCreationForm)

    def test_new_user_saved_after_valid_post(self):
        user_data = create_user_data()
        self.client.post(reverse("home_page:register"), data=user_data)
        self.assertEqual(get_user_model().objects.count(), 1)
        new_user = get_user_model().objects.first()
        self.assertEqual(new_user.username, user_data["username"])

    def test_redirects_with_login_after_valid_post(self):
        user_data = create_user_data()
        response = self.client.post(reverse("home_page:register"), data=user_data)
        self.assertRedirects(response, reverse("home_page:account", args=[user_data["username"]]))

    def test_invalid_input_not_saved(self):
        user_data = create_user_data()
        user_data["password1"] = user_data["username"]
        self.client.post(reverse("home_page:register"), data=user_data)
        self.assertEquals(get_user_model().objects.count(), 0)

    def test_invalid_input_returns_register_template(self):
        user_data = create_user_data()
        user_data["password1"] = user_data["username"]
        response = self.client.post(reverse("home_page:register"), data=user_data)
        self.assertTemplateUsed(response, REGISTER_TEMPLATE)

    def test_invalid_input_returns_register_form(self):
        user_data = create_user_data()
        user_data["password1"] = user_data["username"]
        response = self.client.post(reverse("home_page:register"), data=user_data)
        self.assertIsInstance(response.context["form"], CustomUserCreationForm)

    def test_invalid_input_response_contains_error_message(self):
        user_data = create_user_data()
        user_data["password1"] = user_data["username"]
        response = self.client.post(reverse("home_page:register"), data=user_data)
        self.assertContains(response, "errorlist")


class LoginViewTest(TestCase):
    
    def test_authenticated_user_redirected(self):
        user_data = create_user_data()
        get_user_model().objects.create_user(user_data["username"], user_data["email"], user_data["password1"])
        client = Client()
        client.login(username=user_data["username"], password=user_data["password1"])
        response = client.get(reverse("home_page:login"))
        self.assertRedirects(response, reverse("home_page:account", args=[user_data["username"]]))

    def test_login_template_returned(self):
        response = self.client.get(reverse("home_page:login"))
        self.assertTemplateUsed(response, LOGIN_TEMPLATE)

    def test_login_form_returned(self):
        response = self.client.get(reverse("home_page:login"))
        self.assertIsInstance(response.context["form"], LoginForm)

    def test_user_is_logged_in(self):
        user_data = create_user_data()
        get_user_model().objects.create_user(user_data["username"], 
                                 user_data["email"], 
                                 user_data["password1"])
        response = self.client.post(reverse("home_page:login"), 
                                    data={"username": user_data["username"], 
                                          "password": user_data["password1"]}, 
                                    follow=True)
        print("Response:", response.context["user"])
        self.assertTrue(response.context["user"].is_authenticated)

    def test_user_is_rediredted_after_login(self):
        user_data = create_user_data()
        get_user_model().objects.create_user(user_data["username"], user_data["email"], user_data["password1"])
        response = self.client.post(reverse("home_page:login"), 
                                    data={"username": user_data["username"], 
                                          "password": user_data["password1"]})
        self.assertRedirects(response, reverse("home_page:account", args=[user_data["username"]]))

    def test_invalid_login_returns_login_template(self):
        user_data = create_user_data()
        get_user_model().objects.create_user(user_data["username"], user_data["email"], user_data["password1"])
        incorrect_user_data = create_user_data()
        response = self.client.post(reverse("home_page:login"), 
                                    data={"username": incorrect_user_data["username"],
                                          "password": incorrect_user_data["password1"]})
        self.assertTemplateUsed(response, LOGIN_TEMPLATE)

    def test_invalid_login_response_contains_login_form(self):
        user_data = create_user_data()
        get_user_model().objects.create_user(user_data["username"], user_data["email"], user_data["password1"])
        incorrect_user_data = create_user_data()
        response = self.client.post(reverse("home_page:login"), 
                                    data={"username": incorrect_user_data["username"],
                                          "password": incorrect_user_data["password1"]})
        self.assertIsInstance(response.context["form"], LoginForm)

    def test_invalid_login_contains_error_message(self):
        user_data = create_user_data()
        get_user_model().objects.create_user(user_data["username"], user_data["email"], user_data["password1"])
        incorrect_user_data = create_user_data()
        response = self.client.post(reverse("home_page:login"), 
                                    data={"username": incorrect_user_data["username"],
                                          "password": incorrect_user_data["password1"]})
        self.assertContains(response, "Details did not match an existing user")


class LogoutViewTest(TestCase):

    def test_user_is_redirected(self):
        response = self.client.get(reverse("home_page:logout"))
        self.assertRedirects(response, reverse("home_page:index"))
    
    def test_user_is_logged_out(self):
        user_data = create_user_data()
        get_user_model().objects.create_user(user_data["username"], user_data["email"], user_data["password1"])
        client = Client()
        client.login(username=user_data["username"], password=user_data["password1"])
        response = client.get(reverse("home_page:logout"), follow=True)
        self.assertFalse(response.context["user"].is_authenticated)


class UserViewTest(TestCase):
    
    def test_account_template_returned_for_authenticated_user(self):
        user_data = create_user_data()
        get_user_model().objects.create_user(user_data["username"], user_data["email"], user_data["password1"])
        self.client.login(username=user_data["username"], password=user_data["password1"])
        response = self.client.get(reverse("home_page:account", args=[user_data["username"]]))
        self.assertTemplateUsed(response, ACCOUNT_TEMPLATE)

    def test_existing_user_redirects_to_login(self):
        user_data = create_user_data()
        get_user_model().objects.create_user(user_data["username"], user_data["email"], user_data["password1"])
        response = self.client.get(f"/user/{user_data['username']}")
        self.assertRedirects(response, reverse("home_page:login"))

    def test_new_user_redirects_to_home_page(self):
        user_data = create_user_data()
        get_user_model().objects.create_user(user_data["username"], user_data["email"], user_data["password1"])
        not_registerd_user_data = create_user_data()
        response = self.client.get(reverse("home_page:account", args=[not_registerd_user_data["username"]]))
        self.assertRedirects(response, reverse("home_page:index"))


class DeleteUserView(TestCase):
    
    def test_non_authenticated_user_redirected(self):
        user_data = create_user_data()
        get_user_model().objects.create_user(user_data["username"], user_data["email"], user_data["password1"])
        response = self.client.get(reverse("home_page:delete_account"))
        self.assertRedirects(response, reverse("home_page:login"))

    def test_user_deleted(self):
        user_data = create_user_data()
        get_user_model().objects.create_user(user_data["username"], user_data["email"], user_data["password1"])
        self.client.login(username=user_data["username"], password=user_data["password1"])
        self.client.post(reverse("home_page:delete_account"))
        self.assertEquals(get_user_model().objects.count(), 0)

    def test_user_redirected_after_account_deleted(self):
        user_data = create_user_data()
        get_user_model().objects.create_user(user_data["username"], user_data["email"], user_data["password1"])
        self.client.login(username=user_data["username"], password=user_data["password1"])
        response = self.client.post(reverse("home_page:delete_account"))
        self.assertTemplateUsed(response, DELETE_ACCOUNT_TEMPLATE)

    def test_delete_account_template_returned(self):
        user_data = create_user_data()
        get_user_model().objects.create_user(user_data["username"], user_data["email"], user_data["password1"])
        self.client.login(username=user_data["username"], password=user_data["password1"])
        response = self.client.get(reverse("home_page:delete_account"))
        self.assertTemplateUsed(response, DELETE_ACCOUNT_TEMPLATE)
