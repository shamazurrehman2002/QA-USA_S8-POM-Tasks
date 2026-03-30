from selenium import webdriver
from pages import UrbanRoutesPage
import data
import helpers


class TestUrbanRoutes:

    @classmethod
    def setup_class(cls):
        from selenium.webdriver import DesiredCapabilities

        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome()

        if not helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            raise Exception("Server is not reachable")

    def setup_method(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        self.page = UrbanRoutesPage(self.driver)

    def test_set_address(self):
        self.page.set_addresses(data.FROM_ADDRESS, data.TO_ADDRESS)

        assert self.page.get_from_address() == data.FROM_ADDRESS
        assert self.page.get_to_address() == data.TO_ADDRESS

    def test_select_supportive_plan(self):
        self.page.set_addresses(data.FROM_ADDRESS, data.TO_ADDRESS)
        self.page.click_call_taxi()
        self.page.select_supportive_tariff()

        assert "Supportive" in self.page.get_active_tariff()

    def test_fill_phone_number(self):
        self.page.set_addresses(data.FROM_ADDRESS, data.TO_ADDRESS)
        self.page.click_call_taxi()
        self.page.select_supportive_tariff()

        self.page.enter_phone(data.PHONE_NUMBER)
        code = helpers.retrieve_phone_code(self.driver)
        self.page.enter_sms_code(code)

        assert data.PHONE_NUMBER in self.page.get_phone_value()

    def test_order_blanket(self):
        self.page.set_addresses(data.FROM_ADDRESS, data.TO_ADDRESS)
        self.page.click_call_taxi()
        self.page.select_supportive_tariff()

        self.page.order_blanket_handkerchiefs()

        assert self.page.is_blanket_selected()

    def test_order_taxi(self):
        self.page.set_addresses(data.FROM_ADDRESS, data.TO_ADDRESS)
        self.page.click_call_taxi()
        self.page.select_supportive_tariff()

        self.page.enter_phone(data.PHONE_NUMBER)
        code = helpers.retrieve_phone_code(self.driver)
        self.page.enter_sms_code(code)

        self.page.add_comment(data.MESSAGE_FOR_DRIVER)
        self.page.click_order()

        assert self.page.is_search_modal_displayed()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()