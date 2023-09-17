from django.test import TestCase, RequestFactory, Client
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.urls import reverse
from unittest import skip

from ..home_page_forms import CreateUser, LoginForm
from portfolio.functional_tests.base import FunctionalTest

class IndexViewTest(TestCase):

    def test_index_template_returned(self):
        response = self.client.get(reverse("home_page:index"))
        self.assertTemplateUsed(response, "home_page/index.html")


class RegisterViewTest(TestCase):

    def test_register_template_returned(self):
        response = self.client.get("/register")
        self.assertTemplateUsed(response, "home_page/register.html")

    def test_register_form_returned(self):
        response = self.client.get("/register")
        self.assertIsInstance(response.context["form"], CreateUser)

    def test_new_user_saved_after_valid_post(self):
        functional_test = FunctionalTest()
        username = functional_test.random_user_details(functional_test.UserDetails.USERNAME)
        password = functional_test.random_user_details(functional_test.UserDetails.PASSWORD)
        email = functional_test.random_user_details(functional_test.UserDetails.EMAIL)
        data = {"username": username, 
                "password1": password, 
                "password2": password, 
                "email": email}
        print(data)
        self.client.post("/register", data=data)
        self.assertEqual(User.objects.count(), 1)
        new_user = User.objects.first()
        self.assertEqual(new_user.username, username)

    def test_redirects_with_login_after_valid_post(self):
        functional_test = FunctionalTest()
        username = functional_test.random_user_details(functional_test.UserDetails.USERNAME)
        password = functional_test.random_user_details(functional_test.UserDetails.PASSWORD)
        email = functional_test.random_user_details(functional_test.UserDetails.EMAIL)
        data = {"username": username, 
                "password1": password, 
                "password2": password, 
                "email": email}
        print(data)
        response = self.client.post("/register", data=data)
        self.assertRedirects(response, f"/{username}")

    @skip
    def test_invalid_input_not_saved(self):
        pass

    @skip
    def test_invalid_input_returns_register_template(self):
        pass

    @skip
    def test_invalid_input_returns_register_form(self):
        pass

    @skip
    def test_invalid_input_response_contains_error_message(self):
        pass


class LoginViewTest(TestCase):
    
    @skip
    def test_authenticated_user_redirected(self):
        
        functional_test = FunctionalTest()
        username = functional_test.random_user_details(functional_test.UserDetails.USERNAME)
        password = functional_test.random_user_details(functional_test.UserDetails.PASSWORD)
        email = functional_test.random_user_details(functional_test.UserDetails.EMAIL)
        data = {"username": username, 
                "password1": password, 
                "password2": password, 
                "email": email}
        print(data)

        request_factory = RequestFactory()
        request = request_factory.get(reverse("home_page:login"))

        user = User.objects.create_user(username, email, password)
        user = authenticate(request, username=username, password=password)

        # client = Client()
        # client.login(username=username, password=password)
        request.user = user
        # request.user.is_authenticated = True
        response = self.client.get(reverse("home_page:login"))
        self.assertRedirects(response, f"/{username}")

    def test_login_template_returned(self):
        response = self.client.get("/login")
        self.assertTemplateUsed(response, "home_page/login.html")

    def test_login_form_returned(self):
        response = self.client.get("/login")
        self.assertIsInstance(response.context["form"], LoginForm)

    @skip
    def test_user_is_logged_in(self):
        pass

    @skip
    def test_user_is_rediredted_after_login(self):
        pass

    @skip
    def test_invalid_login_returns_login_template(self):
        pass

    @skip
    def test_invalid_login_shows_error_message(self):
        pass


class LogoutViewTest(TestCase):

    @skip
    def test_user_is_logged_out_and_redirected(self):
        pass


class UserViewTest(TestCase):
    
    @skip
    def test_account_template_returned_for_authenticated_user(self):
        pass

    @skip
    def test_existing_user_redirects_to_login(self):
        pass

    @skip
    def test_new_user_redirects_to_home_page(self):
        pass


class DeleteUserView(TestCase):
    
    @skip
    def test_non_authenticated_user_redirected(self):
        pass

    @skip
    def test_user_deleted_and_redirected(self):
        pass

    @skip
    def test_delete_account_template_returned(self):
        pass
