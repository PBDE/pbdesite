from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from ..forms import CustomCreateUserForm, LoginForm
from portfolio.functional_tests.base import FunctionalTest

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
        self.assertTemplateUsed(response, "home_page/index.html")


class RegisterViewTest(TestCase):

    def test_register_template_returned(self):
        response = self.client.get("/register")
        self.assertTemplateUsed(response, "home_page/register.html")

    def test_register_form_returned(self):
        response = self.client.get("/register")
        self.assertIsInstance(response.context["form"], CustomCreateUserForm)

    def test_new_user_saved_after_valid_post(self):
        user_data = create_user_data()
        self.client.post("/register", data=user_data)
        self.assertEqual(User.objects.count(), 1)
        new_user = User.objects.first()
        self.assertEqual(new_user.username, user_data["username"])

    def test_redirects_with_login_after_valid_post(self):
        user_data = create_user_data()
        response = self.client.post("/register", data=user_data)
        self.assertRedirects(response, f"/{user_data['username']}")

    def test_invalid_input_not_saved(self):
        user_data = create_user_data()
        user_data["password1"] = user_data["username"]
        self.client.post("/register", data=user_data)
        self.assertEquals(User.objects.count(), 0)

    def test_invalid_input_returns_register_template(self):
        user_data = create_user_data()
        user_data["password1"] = user_data["username"]
        response = self.client.post("/register", data=user_data)
        self.assertTemplateUsed(response, "home_page/register.html")

    def test_invalid_input_returns_register_form(self):
        user_data = create_user_data()
        user_data["password1"] = user_data["username"]
        response = self.client.post("/register", data=user_data)
        self.assertIsInstance(response.context["form"], CustomCreateUserForm)

    def test_invalid_input_response_contains_error_message(self):
        user_data = create_user_data()
        user_data["password1"] = user_data["username"]
        response = self.client.post("/register", data=user_data)
        self.assertContains(response, "errorlist")


class LoginViewTest(TestCase):
    
    def test_authenticated_user_redirected(self):
        user_data = create_user_data()
        User.objects.create_user(user_data["username"], user_data["email"], user_data["password1"])
        client = Client()
        client.login(username=user_data["username"], password=user_data["password1"])
        response = client.get(reverse("home_page:login"))
        self.assertRedirects(response, f"/{user_data['username']}")

    def test_login_template_returned(self):
        response = self.client.get("/login")
        self.assertTemplateUsed(response, "home_page/login.html")

    def test_login_form_returned(self):
        response = self.client.get("/login")
        self.assertIsInstance(response.context["form"], LoginForm)

    def test_user_is_logged_in(self):
        
        user_data = create_user_data()
        User.objects.create_user(user_data["username"], 
                                 user_data["email"], 
                                 user_data["password1"])
        response = self.client.post("/login", 
                                    data={"username": user_data["username"], 
                                          "password": user_data["password1"]}, 
                                    follow=True)
        print("Response:", response.context["user"])
        self.assertTrue(response.context["user"].is_authenticated)

    def test_user_is_rediredted_after_login(self):
        user_data = create_user_data()
        User.objects.create_user(user_data["username"], user_data["email"], user_data["password1"])
        response = self.client.post("/login", 
                                    data={"username": user_data["username"], 
                                          "password": user_data["password1"]})
        self.assertRedirects(response, f"/{user_data['username']}")

    def test_invalid_login_returns_login_template(self):
        user_data = create_user_data()
        User.objects.create_user(user_data["username"], user_data["email"], user_data["password1"])
        incorrect_user_data = create_user_data()
        response = self.client.post("/login", 
                                    data={"username": incorrect_user_data["username"],
                                          "password": incorrect_user_data["password1"]})
        self.assertTemplateUsed(response, "home_page/login.html")

    def test_invalid_login_response_contains_login_form(self):
        user_data = create_user_data()
        User.objects.create_user(user_data["username"], user_data["email"], user_data["password1"])
        incorrect_user_data = create_user_data()
        response = self.client.post("/login", 
                                    data={"username": incorrect_user_data["username"],
                                          "password": incorrect_user_data["password1"]})
        self.assertIsInstance(response.context["form"], LoginForm)


    def test_invalid_login_contains_error_message(self):
        user_data = create_user_data()
        User.objects.create_user(user_data["username"], user_data["email"], user_data["password1"])
        incorrect_user_data = create_user_data()
        response = self.client.post("/login", 
                                    data={"username": incorrect_user_data["username"],
                                          "password": incorrect_user_data["password1"]})
        self.assertContains(response, "Invalid login details")


class LogoutViewTest(TestCase):

    def test_user_is_redirected(self):
        response = self.client.get("/logout")
        self.assertRedirects(response, "/")
    
    def test_user_is_logged_out(self):
        user_data = create_user_data()
        User.objects.create_user(user_data["username"], user_data["email"], user_data["password1"])
        client = Client()
        client.login(username=user_data["username"], password=user_data["password1"])
        response = client.get("/logout", follow=True)
        self.assertFalse(response.context["user"].is_authenticated)


class UserViewTest(TestCase):
    
    def test_account_template_returned_for_authenticated_user(self):
        user_data = create_user_data()
        User.objects.create_user(user_data["username"], user_data["email"], user_data["password1"])
        self.client.login(username=user_data["username"], password=user_data["password1"])
        response = self.client.get(f"/{user_data['username']}")
        self.assertTemplateUsed(response, "home_page/account.html")

    def test_existing_user_redirects_to_login(self):
        user_data = create_user_data()
        User.objects.create_user(user_data["username"], user_data["email"], user_data["password1"])
        response = self.client.get(f"/{user_data['username']}")
        self.assertRedirects(response, "/login")

    def test_new_user_redirects_to_home_page(self):
        user_data = create_user_data()
        User.objects.create_user(user_data["username"], user_data["email"], user_data["password1"])
        not_registerd_user_data = create_user_data()
        response = self.client.get(f"/{not_registerd_user_data['username']}")
        self.assertRedirects(response, "/")


class DeleteUserView(TestCase):
    
    def test_non_authenticated_user_redirected(self):
        user_data = create_user_data()
        User.objects.create_user(user_data["username"], user_data["email"], user_data["password1"])
        response = self.client.get("/delete")
        self.assertRedirects(response, "/login")

    def test_user_deleted(self):
        user_data = create_user_data()
        User.objects.create_user(user_data["username"], user_data["email"], user_data["password1"])
        self.client.login(username=user_data["username"], password=user_data["password1"])
        self.client.post("/delete")
        self.assertEquals(User.objects.count(), 0)

    def test_user_redirected_after_account_deleted(self):
        user_data = create_user_data()
        User.objects.create_user(user_data["username"], user_data["email"], user_data["password1"])
        self.client.login(username=user_data["username"], password=user_data["password1"])
        response = self.client.post("/delete")
        self.assertTemplateUsed(response, "home_page/delete_account.html")

    def test_delete_account_template_returned(self):
        user_data = create_user_data()
        User.objects.create_user(user_data["username"], user_data["email"], user_data["password1"])
        self.client.login(username=user_data["username"], password=user_data["password1"])
        response = self.client.get("/delete")
        self.assertTemplateUsed(response, "home_page/delete_account.html")
