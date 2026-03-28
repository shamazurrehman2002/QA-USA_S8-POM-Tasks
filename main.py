from selenium import webdriver
from pages import UrbanRoutesPage
import data
import helpers


class TestUrbanRoutes:

    @classmethod
    def setup_class(cls):
        from selenium.webdriver import DesiredCapabilities

        if not helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            raise Exception("Server is not reachable")

        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome()

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

        assert self.page.get_active_tariff() == "Supportive"

    def test_fill_phone_number(self):
        self.page.set_addresses(data.FROM_ADDRESS, data.TO_ADDRESS)
        self.page.click_call_taxi()
        self.page.select_supportive_tariff()

        code = helpers.retrieve_phone_code(self.driver)
        self.page.add_phone_number(data.PHONE_NUMBER, code)

        assert data.PHONE_NUMBER in self.page.get_phone_value()

    def test_add_credit_card(self):
        self.page.set_addresses(data.FROM_ADDRESS, data.TO_ADDRESS)
        self.page.click_call_taxi()
        self.page.select_supportive_tariff()

        self.page.add_credit_card(data.CARD_NUMBER, data.CARD_CODE)

        assert self.page.get_payment_method() == "Card"

    def test_comment_driver(self):
        self.page.set_addresses(data.FROM_ADDRESS, data.TO_ADDRESS)
        self.page.click_call_taxi()
        self.page.select_supportive_tariff()

        self.page.add_comment(data.MESSAGE_FOR_DRIVER)

        assert self.page.get_comment() == data.MESSAGE_FOR_DRIVER

    def test_order_blanket(self):
        self.page.set_addresses(data.FROM_ADDRESS, data.TO_ADDRESS)
        self.page.click_call_taxi()
        self.page.select_supportive_tariff()

        self.page.order_blanket_handkerchiefs()

        assert self.page.is_blanket_selected() is True

    def test_order_2_ice_creams(self):
        self.page.set_addresses(data.FROM_ADDRESS, data.TO_ADDRESS)
        self.page.click_call_taxi()
        self.page.select_supportive_tariff()

        self.page.order_ice_creams(2)

        assert self.page.get_ice_cream_count() == "2"

    def test_order_taxi(self):
        self.page.set_addresses(data.FROM_ADDRESS, data.TO_ADDRESS)
        self.page.click_call_taxi()
        self.page.select_supportive_tariff()

        code = helpers.retrieve_phone_code(self.driver)
        self.page.add_phone_number(data.PHONE_NUMBER, code)
        self.page.add_comment(data.MESSAGE_FOR_DRIVER)

        self.page.click_order()

        assert self.page.is_search_modal_displayed() is True

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()