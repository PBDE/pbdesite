from django.urls import reverse

## page text
BROWSER_TITLE_TEXT = "PBDE"
HEADER_TEXT = "Hi. I'm"
USER_GREETING_TEXT = "Hi, "

## links
HOME_PAGE_LINK = "<a class='nav-link home-page-link' href='%s'>Home</a>" % reverse("home_page:index")
# LOGIN_LINK = "<a href='%s'>Login</a>" % reverse("home_page:login")
# REGISTER_LINK = "<a href='%s'>Register</a>" % reverse("home_page:register")
# LOGOUT_LINK = "<a href='%s'>Logout</a>" % reverse("home_page:logout")
REGISTER_LINK_TEXT = "Register"
LOGIN_LINK_TEXT = "Login"
LOGOUT_LINK_TEXT = "Logout"
DELETE_ACCOUNT_LINK_TEXT = "Delete Account"

## css ids
# django defaults
ID_USERNAME_INPUT = "id_username"
ID_PASSWORD_INPUT = "id_password"
ID_CREATE_PASSWORD_INPUT = "id_password1"
ID_PASSWORD_CONFIRM_INPUT = "id_password2"
ID_EMAIL_INPUT = "id_email"
ID_OLD_PASSWORD_INPUT = "id_old_password"
ID_NEW_PASSWORD_INPUT = "id_new_password1"
ID_CONFIRM_PASSWORD_INPUT = "id_new_password2"

# own
ID_REGISTER_BTN = "register-btn"
ID_CONFIRM_DELETE_BTN = "confirm-delete-btn"
ID_LOGIN_BTN = "login-btn"
ID_HEADER_TEXT = "header-text-cntr"
# ID_USER_GREETING_TEXT = "user-greeting"
ID_CONFIRMATION_TEXT = "confirm-delete-msg"
ID_DELETED_CONFIRM_TEXT = "account-deleted-msg"
ID_LOGIN_FORM ="login-form"
ID_CREATE_USER_FROM = "create-user-form"
ID_CHANGE_PASSWORD_FORM = "change-password-form"
ID_CHANGE_PASSWORD_BTN = "confirm-change-password-btn"
# ID_FORGOTTEN_PASSWORD_TEXT = "forgetten-password-header"
ID_REQUEST_PASSWORD_BTN = "request-password-btn"
ID_PASSWORD_EMAIL_SENT_TEXT = "password-email-sent-msg"
ID_RESET_PASSWORD_BTN = "password-reset-btn"
ID_PASSWORD_CHANGED_CONFIRM_MSG = "password-changed-confirm-msg"
ID_RETURN_TO_LOGIN_LINK = "login-link"

## css classes
# django defaults
CLS_ERROR_LIST = "errorlist"

# own
CLS_HEADER_TEXT = "header-text-cntr"
CLS_ERROR_TEXT = "form-error-msg"
CLS_SUB_PAGE_HEADER_TEXT = "sub-page-heading"

# messages
CONFIRM_DELETE_ACCOUNT_MSG = "Are you sure you want to delete your account?"
DELETED_ACCOUNT_CONFIRM_MSG = "Account deleted"
USER_DETAILS_ERROR_MSG = "Details did not match an existing user"
PASSWORD_CHANGE_CONFIRMATION_MSG = "Password successfully changed"

# headers
FORGOTTEN_PASSWORD_TEXT = "Forgotten password"
