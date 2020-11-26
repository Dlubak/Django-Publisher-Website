from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from .models import Profile


# Create your tests here.
class AuthorizationTestCase(StaticLiveServerTestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(5)
        super(AuthorizationTestCase, cls).setUpClass()
    
    @classmethod
    def tearDownClass(cls):
        super(AuthorizationTestCase, cls).tearDownClass()
        cls.driver.quit()

    def test_register_with_to_short_password(self):
        submit_xpath = '/html/body/main/div/div[2]/form/div[5]/button'
        self._open_register_page()
        self._fill_register_form('test', '123')
        submit = self.driver.find_element_by_xpath(submit_xpath)
        #Submit form
        submit.send_keys(Keys.RETURN)
        
        response = self.driver.find_element_by_css_selector('body').text
        self.assertTrue('This password is' in response)
        try:
            user = User.objects.get(username='test')
            self.assertIsNotNone(user)
        except User.DoesNotExist:
            pass
        self.assertEqual(f"{self.live_server_url}/register/",
                         self.driver.current_url)

    def test_proper_register_and_check_if_profile_was_created(self):
        submit_xpath = '/html/body/main/div/div[2]/form/div[5]/button'
        self._open_register_page()
        self._fill_register_form('test', 'testPassword123')
        submit = self.driver.find_element_by_xpath(submit_xpath)
        
        #Submit form
        submit.send_keys(Keys.RETURN)
        self.assertIsNotNone(User.objects.get(username='test'))
        self.assertEqual(f"{self.live_server_url}/login/",
                         self.driver.current_url)
        self.driver.implicitly_wait(5)
        try:
            user = User.objects.get(username='test')
            profile = Profile.objects.get(user=user)
        except (User.DoesNotExist, Profile.DoesNotExist):
            pass
        self.assertIsNotNone(profile)
    
    def test_login_page(self):
        self._open_login_page()
        user = User.objects.create(
            username = 'test'
        )
        user.set_password('123')
        user.save()
        self._submit_login_form('test', '123')
        response = self.driver.find_element_by_css_selector('nav').text
        self.assertTrue(user.is_authenticated)
        self.assertTrue('test' in response)

    def _open_register_page(self):
        url = self.live_server_url
        self.driver.get(f'{url}/register/')
        

    def _fill_register_form(self, name, passwd):
        email_xpath = '//*[@id="id_email"]'
        username_xpath = '//*[@id="id_username"]'
        pass_xpath = '//*[@id="id_password1"]'
        pass_conf_xpath = '//*[@id="id_password2"]'
        
        #Get Form
        email = self.driver.find_element_by_xpath(email_xpath)
        username = self.driver.find_element_by_xpath(username_xpath)
        password = self.driver.find_element_by_xpath(pass_xpath)
        password_conf = self.driver.find_element_by_xpath(pass_conf_xpath)

        #Fill the form
        email.send_keys('test@exmaple.com')
        username.send_keys(name)
        password.send_keys(passwd)
        password_conf.send_keys(passwd)
   

    def _open_login_page(self):
        url = self.live_server_url
        self.driver.get(f'{url}/login')
        
    
    def _submit_login_form(self, name, passwd):
        username = self.driver.find_element_by_id('id_username')
        password = self.driver.find_element_by_id('id_password')
        button = self.driver.find_element_by_name('submit')
        username.send_keys(name)
        password.send_keys(passwd)
        button.send_keys(Keys.RETURN)
