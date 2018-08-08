from selenium import webdriver
from selenium.webdriver import ChromeOptions, Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

from threading import Thread

import time
import os



class list_validator(Thread):

    def __init__(self, username, password, link):

        self.username = username
        self.password = password
        self.link = link

        self.creds_valid = None
        self.link_valid = None

        """
        chrome_bin = os.environ.get('GOOGLE_CHROME_SHIM', None)
        opts = ChromeOptions()
        opts.binary_location = chrome_bin
        self.browser = webdriver.Chrome(executable_path="chromedriver", chrome_options=opts)
        """

        options = ChromeOptions()
        options.add_argument("--headless")
        #options.add_experimental_option("detach", True)
        self.browser = webdriver.Chrome(chrome_options=options)


        Thread.__init__(self)

    def run(self):

        browser = self.browser
        print("browser initiated")

        def check_list(browser):
            # ADD TRY EXCEPT: on except, return false

            def destination_valid(browser):
                indicator = browser.find_element_by_id('questionNum')
                if indicator:
                    return True
                else:
                    return False
            
            # make attempt to get link_valid
            # prevents hang if link is completely invalid
            try:
                browser.get(self.link)
            except:
                link_valid = False
                print("link invalid, not real link")
                
            try:
                link_valid = WebDriverWait(browser, 5).until(destination_valid)
                print("link valid")
                print(link_valid)
            except:
                link_valid = False
                print("link invalid")
            
            return link_valid
    

        def check_credentials(browser):

            def destination_valid(browser):
                indicator = browser.find_element_by_xpath('//*[@id="header"]/tbody/tr/td[3]/a[2]')
                if indicator.text == 'Log Out':
                    print('creds valid')
                    return True
                else:
                    print('creds invalid')
                    return False

            browser.get('https://www.vocabtest.com/login.php')
            time.sleep(2) #only until WebDriverWait implemented

            usrField = browser.find_element_by_id("user_login")
            pswdField = browser.find_element_by_id("user_password")

            usrField.send_keys(self.username)
            pswdField.send_keys(self.password)

            logBtn2 = browser.find_element_by_xpath('//*[@id="loginForm"]/a')
            logBtn2.click()

            try:
                creds_valid = WebDriverWait(browser, 6).until(destination_valid)
                print(creds_valid)
            except:
                creds_valid = False
                print(creds_valid)
            
            return creds_valid



        self.link_valid = check_list(browser)
        self.creds_valid = check_credentials(browser)


    def get_creds_valid(self):
        return self.creds_valid

    def get_link_valid(self):
        return self.link_valid

        # FIGURE OUT HOW TO MODIFY INSTANCE CREDS)VALID SO THAT IT IS ACCESSABLE FROM THIS FUNCTINO