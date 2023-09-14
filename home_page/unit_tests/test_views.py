from django.test import TestCase


class IndexViewTest(TestCase):

    def test_index_template_returned(self):
        pass


class RegisterViewTest(TestCase):

    def test_register_template_returned(self):
        pass

    def test_register_form_returned(self):
        pass

    def test_new_user_saved_after_valid_post(self):
        pass

    def test_redirects_with_login_after_valid_post(self):
        pass

    def test_invalid_input_not_saved(self):
        pass

    def test_invalid_input_returns_register_template(self):
        pass

    def test_invalid_input_returns_register_form(self):
        pass

    def test_invalid_input_shows_error_message(self):
        # same test is used in the book
        # but feels like this should be a functional test(?)
        pass


class LoginViewTest(TestCase):
    
    def test_authenticated_user_redirected(self):
        pass

    def test_login_template_returned(self):
        pass

    def test_login_form_returned(self):
        pass

    def test_user_is_logged_in(self):
        pass

    def test_user_is_rediredted_after_login(self):
        pass

    def test_invalid_login_returns_login_template(self):
        pass

    def test_invalid_login_shows_error_message(self):
        pass


class LogoutViewTest(TestCase):

    def test_user_is_logged_out_and_redirected(self):
        pass


class UserViewTest(TestCase):
    
    def test_account_template_returned_for_authenticated_user(self):
        pass

    def test_existing_user_redirects_to_login(self):
        pass

    def test_new_user_redirects_to_home_page(self):
        pass


class DeleteUserView(TestCase):
    
    def test_non_authenticated_user_redirected(self):
        pass

    def test_user_deleted_and_redirected(self):
        pass

    def test_delete_account_template_returned(self):
        pass
