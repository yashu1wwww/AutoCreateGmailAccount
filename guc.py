import undetected_chromedriver as uc
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import random
import time
import sys


class CreateGmail:
    """Auto Create Gmail Accounts with popular names"""

    def __init__(self, firstname, lastname, username, pswd):
        self._firstname = firstname
        self._lastname = lastname
        self._username = username
        self._pswd = pswd
        self._Donefile = open("./data/CreatedAccounts.csv", "a")
        self.Initialize()

    #def Initialize(self):
        #self._browser = webdriver.Chrome()
        #self._browser.delete_all_cookies()
        #self._browser.get("https://accounts.google.com/SignUp?hl=en")

    def Initialize(self):
        driver = uc.Chrome(use_subprocess=True)
        wait = WebDriverWait(driver,20)
        self._browser = uc.Chrome()
        self._browser.delete_all_cookies()
        self._browser.get("https://accounts.google.com/SignUp?hl=en")

    def SetRecoveryEmail(self):
        CreatedEmails = pd.read_csv("./data/CreatedAccounts.csv")["username"].values
        if len(CreatedEmails) < 1:
            self.recovery_email = "pj.cs.vt@gmail.com"
        else:
            self.recovery_email = CreatedEmails[-1] + "@gmail.com"

    def CreateAccount(self):
        # self.SetRecoveryEmail()
        self._browser.find_element_by_css_selector(r'input[id="firstName"]').send_keys(
            self._firstname
        )
        time.sleep(1)
        self._browser.find_element_by_css_selector(r'input[id="lastName"]').send_keys(
            self._lastname
        )
        time.sleep(1)
        self._browser.find_element_by_css_selector(r'input[id="username"]').send_keys(
            self._username
        )
        time.sleep(1)
        self._browser.find_element_by_css_selector(r'input[name="Passwd"]').send_keys(self._pswd)
        time.sleep(3 + 3 * random.random())
        self._browser.find_element_by_css_selector(r'input[name="ConfirmPasswd"]').send_keys(
            self._pswd
        )
        self._browser.find_element_by_css_selector(r'div[id="accountDetailsNext"]').click()
        self._browser.implicitly_wait(10)
        
        self._browser.find_element_by_css_selector('#phoneNumberId').send_keys("9898989898")  #replace with your phone no/use online no for otp verification
        time.sleep(2)
        self._browser.find_element_by_css_selector('#view_container > div > div > div.pwWryf.bxPAYd > div > div.zQJV3 > div > div.qhFLie > div > div > button > span').click()
        time.sleep(15)
        #enter otp within 15 seconds.....remaining all with go automatic.....
        self._browser.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div[1]/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button/span').click()
        time.sleep(2)
        self._browser.find_element_by_css_selector(
                "#month > option:nth-child(%d)" % random.randint(1, 13)
           ).click()
        self._browser.find_element_by_css_selector(r'#day').send_keys("20")
        time.sleep(2)
        self._browser.find_element_by_css_selector(r'#year').send_keys("1994")
        time.sleep(2)
        sex = self._browser.find_element_by_xpath("//*[@id='gender']/option[2]")
        sex.click()
        self._browser.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div[1]/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button/span').click()
        time.sleep(2)
        #webdriver.close()
        self._browser.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div[1]/div[2]/div/div/div[2]/div/div[2]/div[2]/div[1]/div/div/button/span').click()
        time.sleep(2)
        self._browser.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div[1]/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button/span').click()
        time.sleep(30)

    @staticmethod         
    def GetUserInfo (firstnamefile, lastnamefile):
        FirstName = pd.read_csv(firstnamefile).sample(frac=1)
        LastName = pd.read_csv(lastnamefile).sample(frac=1)
        num = min(len(FirstName), len(LastName))
        if len(FirstName) > len(LastName):
           UserInfo = LastName
           UserInfo["firstname"] = FirstName.values[:num]
        else:
            UserInfo = FirstName
            UserInfo["lastname"] = LastName.values[:num]
        UserInfo.index = range(num)
        UserInfo.dropna()
        suffix = ""
        for i in range(6):
            suffix += str(random.randint(0, 9))
        UserInfo["username"] = UserInfo["firstname"] + UserInfo["lastname"] + suffix
        UserInfo["pswd"] = "super" + UserInfo["firstname"] + "233"
        return UserInfo

    def   RunAppsScript(self, sharedlink):
        """So far, cannot auto totally
        
        Open sharedlink and then, plz manually finish Install. 
        """
        self._browser.get(sharedlink)
        time.sleep(10)


if __name__ == "__main__":
    SharedScript = "https://script.google.com/d/1yihwFAHrV17XHYmnrOJxQasqWGourSD57Xi-oFYO3sgY-B1_inPt5Vkc/edit?usp=sharing"

    firstnamefile = "./data/CSV_Database_of_First_Names.csv"
    lastnamefile = "./data/CSV_Database_of_Last_Names.csv"
    UserInfoDF = CreateGmail.GetUserInfo(firstnamefile, lastnamefile)
    for num in range(len(UserInfoDF)):
        UserInfoSeries = UserInfoDF.loc[num]
        CGM = CreateGmail(*UserInfoSeries)
        CGM.CreateAccount()
        # CGM.RunAppsScript(SharedScript)
        time.sleep(10)

            

	