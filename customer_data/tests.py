import socket
import pdb
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import Select
from .models import *
from random import randint

@override_settings(ALLOWED_HOSTS=['*'])  # Disable ALLOW_HOSTS
class CustomerDataTests(StaticLiveServerTestCase):
    """
    Provides base test class which connects to the Docker
    container running Selenium.
    """

    host = '0.0.0.0'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Set host to externally accessible web server address
        cls.host = socket.gethostbyname(socket.gethostname())

        # Instantiate the remote WebDriver
        cls.selenium = webdriver.Remote(
            #  Set to: htttp://{selenium-container-name}:port/wd/hub
            #  In our example, the container is named `selenium`
            #  and runs on port 4444
            command_executor='http://selenium:4444/wd/hub',
            # Set to CHROME since we are using the Chrome container
            desired_capabilities=DesiredCapabilities.CHROME,
        )
        cls.selenium.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def create_project(self, name, company):
        project = Project(
            name = name,
            data = [
                {
                    'year': 1,
                    'revenue': randint(0, 100)
                },
                {
                    'year': 2,
                    'revenue': randint(0, 100)
                },
                {
                    'year': 3,
                    'revenue': randint(0, 100)
                },
                {
                    'year': 4,
                    'revenue': randint(0, 100)
                }
            ],
            company = company
        )
        project.save()

    def buildRecords(self):
        vandelay = Company(name = 'Vandelay Industries')
        vandelay.save()
        gobias = Company(name = 'Gobias Industries')
        gobias.save()
        tobias = User(
            first_name = 'Tobias',
            last_name = 'Funke',
            username = 'tfunke',
            password = 'test'
        )
        tobias.save()
        gob = User(
            first_name = 'GOB',
            last_name = 'Bluth',
            username = 'gbluth',
            password = 'test'
        )
        gob.save()
        tobias.profile.company = gobias
        tobias.profile.save()
        self.create_project('Bees', gobias)
        self.create_project('Coffee', gobias)
        self.create_project('Importer', vandelay)
        self.create_project('Exporter', vandelay)

    def find_by_text(self, text):
        self.selenium.find_element_by_xpath(f"//*[contains(text(), '{text}')]")

    def click_by_text(self, text):
        self.selenium.find_element_by_xpath(f"//*[contains(text(), '{text}')]").click()

    def element_find_by_text(self, text, element):
        self.selenium.find_element_by_xpath(f"//{element}[contains(string(), '{text}')]")

    def element_click_by_text(self, text, element):
        self.selenium.find_element_by_xpath(f"//{element}[contains(string(), '{text}')]").click()

    def select_option(self, text):
        select = Select(self.selenium.find_element_by_id("select-users"))
        select.select_by_visible_text(text)

    def test_projects(self):
        self.buildRecords()
        self.selenium.get(self.live_server_url)
        self.click_by_text('Coffee')
        self.find_by_text('Year 1')
        self.find_by_text('Coffee Chart')

    def test_companies(self):
        self.buildRecords()
        self.selenium.get(self.live_server_url)
        self.click_by_text('Show Companies')
        self.click_by_text('Vandelay Industries')
        self.click_by_text('Importer')
        self.find_by_text('Year 1')
        self.find_by_text('Importer Chart')

    def test_user_assignment_no_refresh(self):
        self.buildRecords()
        self.selenium.get(self.live_server_url)
        self.click_by_text('Show Companies')
        self.click_by_text('Gobias Industries')
        self.element_find_by_text('Tobias Funke', 'li')
        self.selenium.find_element_by_id("select-user").click()
        self.click_by_text('GOB Bluth')
        self.element_click_by_text('Add', 'button')
        self.element_find_by_text('GOB Bluth', 'li')

    def test_user_assignment(self):
        self.buildRecords()
        self.selenium.get(self.live_server_url)
        self.click_by_text('Show Companies')
        self.click_by_text('Gobias Industries')
        self.element_find_by_text('Tobias Funke', 'li')
        self.selenium.find_element_by_id("select-user").click()
        self.click_by_text('GOB Bluth')
        self.element_click_by_text('Add', 'button')
        self.element_find_by_text('GOB Bluth', 'li')

        # Persists after refresh
        self.selenium.get(self.live_server_url)
        self.click_by_text('Show Companies')
        self.click_by_text('Gobias Industries')
        self.element_find_by_text('GOB Bluth', 'li')

    def test_can_change_user_assignment(self):
        self.buildRecords()

        # Assign GOB to Vandelay
        gob_profile = User.objects.filter(first_name='GOB')[0].profile
        gob_profile.company = Company.objects.filter(name='Vandelay Industries')[0]
        gob_profile.save()

        self.selenium.get(self.live_server_url)
        self.click_by_text('Show Companies')
        self.click_by_text('Gobias Industries')
        self.element_find_by_text('Tobias Funke', 'li')
        self.selenium.find_element_by_id("select-user").click()
        self.click_by_text('GOB Bluth')
        self.element_click_by_text('Add', 'button')
        self.element_find_by_text('GOB Bluth', 'li')

        # Removed from Vandelay company page
        self.click_by_text('Vandelay Industries')
        try:
            self.element_find_by_text('GOB Bluth', 'li')
            not_found = False
        except:
            not_found = True

        assert not_found

    def test_user_assignment_dropdown_only_has_available_users(self):
        self.buildRecords()

        # Assign GOB to Vandelay
        gob_profile = User.objects.filter(first_name='GOB')[0].profile
        gob_profile.company = Company.objects.filter(name='Vandelay Industries')[0]
        gob_profile.save()

        self.selenium.get(self.live_server_url)
        self.click_by_text('Show Companies')
        self.click_by_text('Gobias Industries')
        self.element_find_by_text('Tobias Funke', 'li')
        self.selenium.find_element_by_id("select-user").click()

        try:
            self.selenium.find_element_by_xpath("//*[contains(@class, 'MuiMenuItem-root') and contains(text(), 'Tobias Funke')]")
            not_found = False
        except:
            not_found = True

        assert not_found
