from pages.base_page import BasePage
from locators.login_locators import LoginLocators

class LoginPage(BasePage):
    def __init__(self, page, base_url):
        super().__init__(page, base_url)
        self.locators = LoginLocators

    def login(self, email: str, password: str):
        """Fills in credentials and submits the login form."""
        self.fill_text(self.locators.EMAIL_INPUT, email)
        self.fill_text(self.locators.PASSWORD_INPUT, password)
        self.click(self.locators.LOGIN_BUTTON)

