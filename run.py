from  common.session import session
from common.base_login import base_login
from common.files_utils import files_utils
from common.ui_utils import ui_utils
from selenium.webdriver.common.by import By
from pprint import pprint
from common.navigate import navigate

import os
import traceback
import time
import sys
from common.timesheet_page import timesheet_page
from common.otp_utils import otp_utils


class run(object):

    ses = None
    otp_utils = None
    ui_utils = None
    navigate = None
    timesheet_page = None

    def getSessionAndLogin(self):
        self.otp_utils = otp_utils()

        if self.ses == None:
            self.ses = session()
            ses = self.ses
            self.ui_utils = ui_utils(self.ses)
            self.navigate = navigate(self.ses)
            if self.ses.FIREFOX_DOWNLOAD_DIR.startswith("./"):
                self.ses.FIREFOX_DOWNLOAD_DIR = os.path.dirname(os.path.realpath(__file__)) + "/" + self.ses.FIREFOX_DOWNLOAD_DIR
            files_utils.remove(self.ses, self.ses.FIREFOX_DOWNLOAD_DIR)
            os.mkdir(self.ses.FIREFOX_DOWNLOAD_DIR)
            #os.mkdir(self.ses.FIREFOX_DOWNLOAD_DIR + "/debug")
            downloadDebugDir=self.ses.FIREFOX_DOWNLOAD_DIR+"/debug"
            #files_utils.remove(self.ses, downloadDebugDir)

            if "True" in self.ses.DEBUG:
                os.mkdir(downloadDebugDir)

            out, err = self.otp_utils.generatePassword(self.ses.LOGIN_PASSWORD_GENERATOR_COMMAND)
            if err is not None:
                pprint("Something went wrong with getting OTP token code .. exiting. Bye.")
                self.ses.close_web_driver()
                exit(1)

            password = out.decode("utf-8") .replace("\n","").replace("'","").replace("b","")

            base_login(ses).login(ses.LOGIN_USERNAME, self.ses.LOGIN_PASSWORD_PREFIX + password)

    def magic(self):
        pprint("Sparkles *** ")
        self.getSessionAndLogin()
        self.navigate.get(self.ses.BASE_URL + self.ses.URL_TIMESHEET, self.ses.TX_URL_TIMESHEET)

        self.timesheet_page = timesheet_page(self.ui_utils)
        self.timesheet_page.fillTimesheet()
        pass
