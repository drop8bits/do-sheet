import time
#from webbrowser import browser

from selenium.common.exceptions import NoSuchElementException
from common.files_utils import files_utils
from common.timeout import timeout

class ui_utils():

    web_session = None
    web_driver = None

    WAIT_VERY_SHORT=30
    WAIT_SHORT=30
    WAIT_MEDIUM=60
    WAIT_LONG=300
    WAIT_EXTRA_LONG=600
    WAIT_EXTRA_SUPER_LONG=3600

    def __init__(self, web_session):
        self.web_session = web_session
        self.web_driver = web_session.web_driver
        self.WAIT_VERY_SHORT = int(web_session.WAIT_VERY_SHORT)
        self.WAIT_SHORT = int(web_session.WAIT_SHORT)
        self.WAIT_MEDIUM = int(web_session.WAIT_MEDIUM)
        self.WAIT_LONG = int(web_session.WAIT_LONG)
        self.WAIT_EXTRA_LONG = int(web_session.WAIT_EXTRA_LONG)
        self.WAIT_EXTRA_SUPER_LONG = int(web_session.WAIT_EXTRA_SUPER_LONG)

    def isTextOnPage(self, text):
        # Just visible text - http://stackoverflow.com/a/651801
        if self.web_driver.find_elements_by_xpath(".//*[contains(text(), '" + text + "') and not (ancestor::*[contains( @ style,'display:none')]) and not (ancestor::*[contains( @ style, 'display: none')])]"):
            return True
        else:
            return False

    # if exist=False then we wait till texts disappears (waitTillTextOnPage[Not]Exists)
    def waitForTextOnPage(self, text, waitTime, exist=True, refresh=False):
        waitTime=int(waitTime)
        try:
            text=text.encode("iso-8859-2").decode("UTF-8")
        except UnicodeDecodeError as ude:
            text=text

        if exist:
            self.web_session.logger.info("Waiting " + str(waitTime) + " seconds for text: " + text)
        else:
            self.web_session.logger.info("Waiting " + str(waitTime) + " seconds text to dissapear: " + text)
        currentTime = time.time()
        isTextOnPage = self.isTextOnPage(text)
        while (( not isTextOnPage and exist ) or
                   ( isTextOnPage and not exist )) :
            if time.time() - currentTime >= waitTime:
                self.web_session.logger.info("Timed out waiting for: %s", text)
                if "Strict" in self.web_session.DEBUG:
                    files_utils.createScreenshot(self.web_session,"waitForTextOnPage-" + files_utils.simpleStr(text))
                return False
            else:
                if not exist and refresh:
                    self.web_driver.refresh()
                #time.sleep(1)
            time.sleep(1)
            self.web_session.logger.info("Waiting for '" + text + "' in UI")
            isTextOnPage = self.isTextOnPage(text)
        return True

    def isElementPresent(self, locatormethod, locatorvalue):
        try:
            self.web_driver.find_element(by=locatormethod, value=locatorvalue)
        except NoSuchElementException:
            return False
        return True

    def waitForElementOnPage(self, locatormethod, locatorvalue, waitTime, exist=True, refresh=False, show_as_error=True):
        currentTime = time.time()
        waitTime=int(waitTime)
        self.closePossibleModalDialog()
        isElementPresent = self.isElementPresent(locatormethod, locatorvalue)
        self.closePossibleModalDialog()
        while ((not isElementPresent and exist) or
                   (isElementPresent and not exist)):
            self.closePossibleModalDialog()
            if time.time() - currentTime >= waitTime:
                if show_as_error:
                    self.web_session.logger.error("Timed out waiting for: %s", locatorvalue)
                else:
                    self.web_session.logger.info("Timed out waiting for: %s", locatorvalue)
                if "Strict" in self.web_session.DEBUG:
                    files_utils.createScreenshot(self.web_session,"waitForElementOnPage-" + files_utils.simpleStr(locatorvalue))
                return False
            else:
                if not exist and refresh:
                    self.web_driver.refresh()
                time.sleep(1)
                isElementPresent = self.isElementPresent(locatormethod, locatorvalue)

        return True


    def wait_until_element_displayed(self, element, waitTime):

        with timeout(waitTime, error_message="Timed out waiting for element to be displayed."):
            while True:
                if element.is_displayed():
                    break;
                time.sleep(1)

        return True

    def sleep(self, waitTime):
        time.sleep(waitTime)

    def adjust_screen_resolution(self, horizontal, vertical):
        self.web_driver.set_window_size(horizontal, vertical)
