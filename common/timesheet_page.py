from datetime import datetime
from pprint import pprint

class timesheet_page():

    ui_utils = None
    ses = None
    rows = []
    now = datetime.now()

    def __init__(self, ui_utils):
        self.ui_utils = ui_utils
        self.ses = ui_utils.web_session
        pass

    def representsInt(s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    def parseLineValueToXpathSubstring(self, line):
        if line.count("-") == 2:
            return "//label[contains(text(),'"+line+"')]/../.."
        if self.representsInt(line):
            return self.ses.XP_TIMESHEET_ACTIVE_ROWS+"["+str(line)+"]"
        return line

    def setFiled(self, row, xpathPostfix, value, override = False):
        xpath = "[" + row + "]" + self.ses.XP_TIMESHEET_ACTIVE_ROWS + xpathPostfix
        pprint(xpath)
        elem = self.ui_utils.web_driver.find_element_by_xpath(xpath)
        elem_value = elem.get_attribute("value")
        if ((elem_value  is None or elem_value is "") or
                (override is True or "True" in self.ses.OVERRIDE_EVERY_VALUE)):
            elem.send_keys(value)
        else:
            pprint("For xpath: " + xpath + " value already exist: " + elem_value)
        pass

    def setStartTime(self, row, value):
        self.setFiled(row, self.ses.XP_START_TIME,value)
        pass

    def setEndTime(self, row, value):
        self.setFiled(row,  self.ses.XP_END_TIME,value)

    def setBreakTime(self, row, value):
        self.setFiled(row,  self.ses.XP_BREAK_TIME,value)
        pass

    def setComment(self, row, value):
        self.setFiled(row,  self.ses.XP_COMMENT,value)
        pass

    def save(self):
        elem = self.ui_utils.web_driver.find_element_by_xpath(self.ses.XP_TIMESHEET_BTN_SAVE)
        elem.click()
        self.ui_utils.waitForTextOnPage(self.ses.TX_TIMESHEET_BTN_SUBMIT)
        pass

    def submit(self):
        elem = self.ui_utils.web_driver.find_element_by_xpath(self.ses.XP_TIMESHEET_BTN_SUBMIT)
        elem.click()
        self.ui_utils.waitForTextOnPage(self.ses.XT_TIMESHEET_BTN_SAVE)
        pass

    def getRows(self):
        self.rows = self.ui_utils.web_driver.find_elements_by_xpath(self.ses.XP_TIMESHEET_ACTIVE_ROWS)
        pass

    def fillTimesheet(self):
        self.getRows()
        for row_ in range(1,len(self.rows)+1):
            rowIndex = str(row_)
            row = self.ui_utils.web_driver.find_element_by_xpath(
                self.ses.XP_TIMESHEET_ACTIVE_ROWS + "["+rowIndex+"]//label")
            possibleDateStr = row.text
            day = datetime.strptime(possibleDateStr, '%d-%b-%Y')
            dayInWeek = str(day.weekday())

            if "True" in self.ses.APPEND_TILL_TODAY:
                if (self.now - day).days >= 0:
                    continue
                if "True" in self.ses.APPEND_ONLY_ONE and (self.now - day).days >= 1:
                    break
                pass

            #pprint(row)
            #pprint(day)
            #pprint(dayInWeek)

            if "True" in self.ses.USE_WEEK_DAY_PREFIX:
                start = self.getattr(self.ses,"WEEK_DAY_" + dayInWeek + "_START")
                end = self.getattr(self.ses, "WEEK_DAY_" + dayInWeek + "_END")
                break_ = self.getattr(self.ses, "WEEK_DAY_" + dayInWeek + "_BREAK")
                comment = self.getattr(self.ses, "WEEK_DAY_" + dayInWeek + "_COMMENT")
                # TODO
                commentRandomText = self.getattr(self.ses, "WEEK_DAY_" + dayInWeek + "_RANDOM_TEXT")
                commentRandomConfig = self.getattr(self.ses, "WEEK_DAY_" + dayInWeek + "_RANDOM_TEXT_CONFIG")

                finalComment = self.generateComment(start, end, break_, comment, commentRandomText, commentRandomConfig)
                self.handleRowFill(rowIndex, start, end, break_, finalComment)
                pass

            if "True" in self.ses.USE_ALL_DAY_PREFIX:
                # TODO
                arr = self.ses.propertiesByPrefix("ALL_DAY_")
                pass
            # TODO use REGEX_DAY_PREFIX

        if "True" in self.ses.SAVE_AUTOMATICALLY:
            self.timesheet_page.save()
        if "True" in self.ses.SUBMIT_AUTOMATICALLY:
            self.timesheet_page.submit()

        pass

    def handleRowFill(self, rowI, start, end, break_, comment):
        self.setStartTime(rowI,start)
        self.setEndTime(rowI,end)
        self.setBreakTime(rowI,break_)
        self.setComment(rowI,comment)
        pass

    def getattr(self, item, attr):
        try:
            ret = getattr(item, attr)
            return ret
        except AttributeError:
            return ""
        pass

    def generateComment(self, start, end, break_, comment, commentRandomText, commentRandomConfig):
        return comment

