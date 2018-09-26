from selenium.webdriver.common.keys import Keys
from common.navigate import navigate
from common.ui_utils import ui_utils

class base_login(object):
    web_session = None
    web_driver = None


    def __init__(self, web_session):
        self.web_session = web_session
        self.web_driver = web_session.web_driver

    def login(self, username, password):
        self.web_session.logger.info("Login with:")
        self.web_session.logger.info(self.web_session.BASE_URL)
        self.web_session.logger.info(self.web_session.BASE_LOGIN_PATH)
        navigate(self.web_session).get("{}".format(self.web_session.BASE_URL + self.web_session.BASE_LOGIN_PATH), wait_for=self.web_session.TX_SIGNIN)
        self.username = username
        self.password = password

        elem = self.web_driver.find_element_by_xpath(self.web_session.XP_LOGIN_PAGE_USERNAME)
        elem.send_keys(self.username)
        elem = self.web_driver.find_element_by_xpath(self.web_session.XP_LOGIN_PAGE_PASSWORD)
        elem.send_keys(self.password)
        elem.send_keys(Keys.RETURN)
        #import unicodedata
        assert ui_utils(self.web_session).waitForTextOnPage(self.web_session.TX_LOGIN, 300)
