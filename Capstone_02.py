from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import unittest


# Locators and Configurations for OrangeHRM
class OrangeHRM_Locators:
    username = "username"
    password = "password"
    submit_button = "//button[@type='submit']"
    url = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
    dashboard_url = "https://opensource-demo.orangehrmlive.com/web/index.php/dashboard/index"
    excel_file = "D:\\workspace\\Python_Workspace\\DDTF\\Data\\test_data.xlsx"
    sheet_number = "Sheet1"
    pass_data = "TEST PASS"
    fail_data = "TEST FAILED"


# Page Object for Login Page
class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.username_input = (By.NAME, OrangeHRM_Locators.username)
        self.password_input = (By.NAME, OrangeHRM_Locators.password)
        self.login_button = (By.XPATH, OrangeHRM_Locators.submit_button)
        self.forgot_password_link = (By.LINK_TEXT, "Forgot your password?")
        self.success_message = (By.XPATH, "//div[contains(text(), 'Reset Password link sent successfully')]")

    def open(self):
        self.driver.get(OrangeHRM_Locators.url)

    def click_forgot_password(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.forgot_password_link)
        ).click()

    def enter_username(self, username):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.username_input)
        ).send_keys(username)

    def enter_password(self, password):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.password_input)
        ).send_keys(password)

    def click_login(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.login_button)
        ).click()

    def get_success_message(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.success_message)
        ).text


# Page Object for Admin Page
class AdminPage:
    def __init__(self, driver):
        self.driver = driver
        self.page_title = (By.TAG_NAME, "h1")
        self.menu_items = {
            "User Management": (By.LINK_TEXT, "User Management"),
            "Job": (By.LINK_TEXT, "Job"),
            "Organization": (By.LINK_TEXT, "Organization"),
            "Qualifications": (By.LINK_TEXT, "Qualifications"),
            "Nationalities": (By.LINK_TEXT, "Nationalities"),
            "Corporate Banking": (By.LINK_TEXT, "Corporate Banking"),
            "Configuration": (By.LINK_TEXT, "Configuration"),
        }

    def validate_title(self):
        title = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.page_title)
        ).text
        return title

    def validate_menu_items(self):
        for item_name, locator in self.menu_items.items():
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(locator)
            )


# Test cases for OrangeHRM
class TestForgotPassword(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.login_page = LoginPage(self.driver)
        self.login_page.open()

    def test_forgot_password(self):
        self.login_page.click_forgot_password()
        self.login_page.enter_username("Admin")
        self.login_page.click_login()  # Click on reset password button
        success_message = self.login_page.get_success_message()
        self.assertEqual(success_message, "Reset Password link sent successfully")

    def tearDown(self):
        self.driver.quit()


class TestAdminPage(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.login_page = LoginPage(self.driver)
        self.admin_page = AdminPage(self.driver)

        # Log in as Admin
        self.login_page.open()
        self.login_page.enter_username("Admin")
        self.login_page.enter_password("admin123")  # Assuming the password is "admin123"
        self.login_page.click_login()

    def test_header_validation(self):
        title = self.admin_page.validate_title()
        self.assertEqual(title, "OrangeHRM")  # Assuming "OrangeHRM" is the expected title

    def test_menu_validation(self):
        self.admin_page.validate_menu_items()  # This will check if menu items are visible

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
