from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class UrbanRoutesPage:
    # Locators
    FROM_FIELD = (By.ID, "from")
    TO_FIELD = (By.ID, "to")

    CALL_TAXI_BUTTON = (By.XPATH, "//button[text()='Call a taxi']")
    SUPPORTIVE_TARIFF = (By.XPATH, "//div[contains(text(),'Supportive')]")
    ACTIVE_TARIFF = (By.XPATH, "//div[contains(@class,'tcard active')]")

    PHONE_FIELD = (By.ID, "phone")
    NEXT_BUTTON = (By.XPATH, "//button[text()='Next']")
    CODE_FIELD = (By.ID, "code")
    CONFIRM_BUTTON = (By.XPATH, "//button[text()='Confirm']")

    PAYMENT_METHOD = (By.CLASS_NAME, "pp-value-text")
    ADD_CARD_BUTTON = (By.XPATH, "//div[text()='Add card']")
    CARD_NUMBER_FIELD = (By.ID, "number")
    CARD_CODE_FIELD = (By.ID, "code")
    LINK_BUTTON = (By.XPATH, "//button[text()='Link']")

    COMMENT_FIELD = (By.ID, "comment")

    BLANKET_SWITCH = (By.XPATH, "//span[@class='slider round']")
    BLANKET_CHECKBOX = (By.XPATH, "//input[@type='checkbox']")

    ICE_CREAM_PLUS = (By.XPATH, "//div[contains(@class,'counter-plus')]")
    ICE_CREAM_COUNT = (By.CLASS_NAME, "counter-value")

    ORDER_BUTTON = (By.XPATH, "//button[text()='Order']")
    SEARCH_MODAL = (By.CLASS_NAME, "order-header")

    def __init__(self, driver):
        self.driver = driver

    def set_addresses(self, from_address, to_address):
        self.driver.find_element(*self.FROM_FIELD).send_keys(from_address)
        self.driver.find_element(*self.TO_FIELD).send_keys(to_address)

    def get_from_address(self):
        return self.driver.find_element(*self.FROM_FIELD).get_attribute("value")

    def get_to_address(self):
        return self.driver.find_element(*self.TO_FIELD).get_attribute("value")

    def click_call_taxi(self):
        self.driver.find_element(*self.CALL_TAXI_BUTTON).click()

    def select_supportive_tariff(self):
        tariff = self.driver.find_element(*self.SUPPORTIVE_TARIFF)
        active = self.driver.find_element(*self.ACTIVE_TARIFF)

        if "active" not in active.get_attribute("class"):
            tariff.click()

    def get_active_tariff(self):
        return self.driver.find_element(*self.ACTIVE_TARIFF).text

    def add_phone_number(self, phone, code):
        self.driver.find_element(*self.PHONE_FIELD).send_keys(phone)
        self.driver.find_element(*self.NEXT_BUTTON).click()
        self.driver.find_element(*self.CODE_FIELD).send_keys(code)
        self.driver.find_element(*self.CONFIRM_BUTTON).click()

    def get_phone_value(self):
        return self.driver.find_element(*self.PHONE_FIELD).get_attribute("value")

    def add_credit_card(self, number, code):
        self.driver.find_element(*self.PAYMENT_METHOD).click()
        self.driver.find_element(*self.ADD_CARD_BUTTON).click()
        self.driver.find_element(*self.CARD_NUMBER_FIELD).send_keys(number)

        code_field = self.driver.find_element(*self.CARD_CODE_FIELD)
        code_field.send_keys(code)
        code_field.send_keys(Keys.TAB)

        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.LINK_BUTTON)
        ).click()

    def get_payment_method(self):
        return self.driver.find_element(*self.PAYMENT_METHOD).text

    def add_comment(self, message):
        self.driver.find_element(*self.COMMENT_FIELD).send_keys(message)

    def get_comment(self):
        return self.driver.find_element(*self.COMMENT_FIELD).get_attribute("value")

    def order_blanket_handkerchiefs(self):
        self.driver.find_element(*self.BLANKET_SWITCH).click()

    def is_blanket_selected(self):
        return self.driver.find_element(*self.BLANKET_CHECKBOX).get_property("checked")

    def order_ice_creams(self, amount):
        for _ in range(amount):
            self.driver.find_element(*self.ICE_CREAM_PLUS).click()

    def get_ice_cream_count(self):
        return self.driver.find_element(*self.ICE_CREAM_COUNT).text

    def click_order(self):
        self.driver.find_element(*self.ORDER_BUTTON).click()

    def is_search_modal_displayed(self):
        return self.driver.find_element(*self.SEARCH_MODAL).is_displayed()