from selenium import webdriver
from selenium.webdriver import ChromeOptions, Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

from threading import Thread
import time
import os






class list_solver(Thread):

    
    
    
    
    
    
    # FOLLOWING FUNCTIONS ENCLOSED CAN BE MIGRATED TO PARENT CLASS IN FUTURE IF NEED BE
    # THIS CLASS (WHICH IS A SPECIFIC FUNCTION) can inherit the parent class.
    # it would inherit init, percent done, etc.
    # only NEEDED if additional functionality on the website was added (splitting up learning and solving)
    
    

    
    def __init__(self, link, username, password, email):
        
        self.link = link
        self.username = username
        self.password = password
        self.email = email
        
        self.word_list = {}
        self.list_length = 1
        self.completedWords = 0
        self.currentWord = ""
        self.correctDefinition = ""
        self.currentOperation = ""
        self.currentCommand = ""
        self.iterations = 1
        self.ellapsedTime = 0
        self.initTime = time.time() #time of initialization
        self.loggedIn = None
        self.listType = ""

        self.debugging_enabled = False

        """
        chrome_bin = os.environ.get('GOOGLE_CHROME_SHIM', None)
        opts = ChromeOptions()
        opts.binary_location = chrome_bin
        self.browser = webdriver.Chrome(executable_path="chromedriver", chrome_options=opts)
        """

        options = ChromeOptions()
        #options.add_argument("--headless")
        options.add_experimental_option("detach", True)
        self.browser = webdriver.Chrome(chrome_options=options)
        
        Thread.__init__(self)
    
    
    def run(self):
        
        
        # BEGINNING OF PROCESS DEPENDENT VARIABLES
        
        
        choiceList = ['a', 'b', 'c', 'd', 'e']  # CORRESPONDING SENDABLE KEY VALUES
        timeThreshold = 20  # Wating threshold for WebDriverWait
        loginLink = 'https://www.vocabtest.com/login.php'
        
        
        

        # CREATE HEALDESS CHROME INSTANCE
        #   - use browser from instance in usable format
        browser = self.browser
        
        
        
        
        # BEGINNING OF PROCESS-SPEICIFIC ALTERNATE FUNCTIONALITY FUNCTIONS
        # INCLUDED: SEND RESULTS ...
        
        def get_list_length(browser):
            
            self.currentOperation = "getting list length"
            indicator = browser.find_element_by_id('questionNum')
            length = indicator.text
            num, length = length.split('/')
            self.list_length = int(length)
        
        def get_list_type(browser):
            
            url = browser.current_url
            if "sentences" in url:
                self.listType = "sentences"


        def login(browser, usr, pswd):
            
            def destination_valid(browser):
                indicator = browser.find_element_by_xpath('//*[@id="header"]/tbody/tr/td[3]/a[2]')
                if indicator.text == 'Log Out':
                    return True
                else:
                    return False
            
            self.currentCommand = "logging in " + usr
            self.currentOperation = "logging in"
            
            time.sleep(2)   # ADD WAITING FOR USERFIELD TO LOAD (might not needed as it waits until refresh)

            usrField = browser.find_element_by_id("user_login")
            pswdField = browser.find_element_by_id("user_password")

            usrField.send_keys(usr)
            pswdField.send_keys(pswd)

            logBtn2 = browser.find_element_by_xpath('//*[@id="loginForm"]/a')
            logBtn2.click()
            
            try:
                loggedIn = WebDriverWait(browser, 6).until(destination_valid)
                return True
            except:
                print("login not successful for "  + usr)
                return False
                
                         
        def send_results(browser, email):
            
            def email_loaded(browser):
                elem = browser.find_element_by_xpath('//*[@id="emailTo"]')
                if elem:
                    return elem
                else:
                    return False
            
            self.currentOperation = "sending results"
            
            try:
                emailField = WebDriverWait(browser, timeThreshold).until(email_loaded)
            except:
                print("Email field not present, list not completed")
                # add system to reenter list solving
                
            emailField.send_keys(email)
            
            sendBtn = browser.find_element_by_xpath('//*[@id="contentHolder"]/form/div[2]/input[5]')
            sendBtn.click()
            print("sending results complete")
        

        def save_list(browser):
            saveButton = browser.find_element_by_id('saveButton')
            saveButton.click()


        def view_results(browser):
            pass # add ability to go to completed lists

            
        def print_message(message):
            linkDetail = self.link.split('?')
            
            if self.debugging_enabled:
                print('')
                print("INSTANCE: " + self.username + " | " + self.email + " | " + linkDetail[1])
                print("MESSAGE: " + message)
                print('')
            else:
                pass     
        
        '''
        def restart_session(browser, url):
            print("previous browser: " + str(browser))
            browser.quit()
            
            options = ChromeOptions()
            options.add_argument("--headless")
            #options.add_experimental_option("detach", True)
            self.browser = webdriver.Chrome(chrome_options=options)
            print("new browser: " + str(self.browser))
            self.browser.get(url)
            return self.browser
        '''
        

        
        # BEGINNING OF SOLVER DEPENDENT FUNCTIONS
        #   - Made dynamic per browser, page, etc.
        #   - Potentially make this independent class, have "process" class extend this


        def elimCSS(browser):
            page = browser.find_element_by_tag_name('body')
            browser.execute_script("document.head.parentNode.removeChild(document.head);", page)
        
            
        def is_duplicate(word):
            for words in self.word_list:
                if words == word:
                    return True     #if true, duplicate present
            return False


        def word_loaded(browser):
            elem = browser.find_element_by_id("qnaBody-" + str(self.iterations))
            if elem:
                if self.listType == "sentences":
                    question = elem.find_element_by_class_name('question')
                    return question

                word = elem.find_element_by_class_name('question')
                word = word.find_element_by_tag_name('b')
                return word
            else:
                return False
            
            
        def answerButtons_loaded(browser):
            elem = browser.find_element_by_id("qnaBody-" + str(self.iterations))
            if elem:
                answerButtons = elem.find_element_by_id('answerButtonsHolder')
                answerButtons = answerButtons.find_elements_by_tag_name('a')
                return answerButtons
            else:
                return False
            

        def definitions_loaded(browser):
            elem = browser.find_element_by_id("qnaBody-" + str(self.iterations))
            if elem:
                definitions = elem.find_element_by_id('answerTextHolder')
                definitions = definitions.find_elements_by_tag_name('li')
                return definitions
            else:
                return False
    

    
    
        # NAVIGATE TO LIST
        browser.get(self.link)
        elimCSS(browser)    #decreases loadingtimes
        get_list_length(browser)
        get_list_type(browser)
        #print(self.list_length)
        


        
        # BEGINNING OF PROCESS (LEARNING LIST)
        #   - put into TRY / EXCEPT format to handle errors

        print(self.listType)
        while(len(self.word_list) < self.list_length):
            
            self.currentOperation = "learning list"
            print_message("Iterations: " + str(self.iterations))
            
            try:
                vocabWord = WebDriverWait(browser, timeThreshold).until(word_loaded)
                definitions = WebDriverWait(browser, timeThreshold).until(definitions_loaded)
                answerButtons = WebDriverWait(browser, timeThreshold).until(answerButtons_loaded)
            except:
                # ESSENTIAL TO ENSURE THAT PROCESS DOESN'T GET HUNG UP ON WAITING FOR ELEMENT ON PAGE
                # REFRESH IN ORDER TO HAVE ELEMENTES LOAD AGAIN
                print_message("Elements not loaded, reloading page")
                self.currentCommand = "Reloading page, elements failed to load"
                
                browser.refresh()
                elimCSS(browser)

                self.iterations = 1
                
                continue
            
            #print('')
            #print(vocabWord.text + " updated: " + " qnaBODY " + str(self.iterations))   #debugging
            
            found = False
            for x, button in enumerate(answerButtons):
                
                button.click()
                time.sleep(.2)
                
                if button.text == '✓':
                    self.correctDefinition = definitions[x].text
                    
                    if(is_duplicate(vocabWord.text)):
                        #print("!!Duplicate Word!!") #debugging
                        self.currentCommand = (vocabWord.text).upper() + ": duplicate, already found"
                    
                    else:
                        self.word_list[vocabWord.text] = self.correctDefinition
                        self.currentCommand = (vocabWord.text).upper() + ": " + self.correctDefinition
                    
                    break
                    
                #time.sleep(.1)  #evaluation delay (DECREASE)
            
            self.iterations += 1
            self.completedWords = len(self.word_list)
        
        
        
        
        # BEGINNING OF LOGIN PROCESS
        #   - consider making jquery wait to get progress until after finished?
        
        
        browser.get(loginLink)
        elimCSS(browser)
        
        # Ensures that login process bypasses browser hang
        self.loggedIn = login(browser, self.username, self.password)
        while not self.loggedIn:
            loggedIn = login(browser, self.username, self.password)
        
        browser.get(self.link)
        elimCSS(browser)
        
        # iterations only used to index qna body elements
        # as the do NOT affect process_progress
        self.iterations = 1
        
        
        
        
        # BEGINNING OF PORCESS (SOLVING LIST)
        
        i = 0
        while i < self.list_length:
            
            self.currentOperation = "solving list"
            print_message("Iterations: " + str(self.iterations) + " | Loop: " + str(i))

            try:
                vocabWord = WebDriverWait(browser, timeThreshold).until(word_loaded)
                definitions = WebDriverWait(browser, timeThreshold).until(definitions_loaded)
                answerButtons = WebDriverWait(browser, timeThreshold).until(answerButtons_loaded)
                #print(vocabWord.text)   #debugging
            except:
                # step loop maximum up
                # reset iterations for finding qnabody
                i -= 1
                self.iterations = 1
                # report error
                print_message("Elements not loaded, reloading page")
                self.currentCommand = "Reloading page, elements failed to load"
                #browser = restart_session(browser, self.link)
                save_list(browser)
                browser.refresh()
                elimCSS()

                continue
                
            
            for word in self.word_list:
                if word == vocabWord.text:
                    self.correctDefinition = self.word_list[word]
                    #print(self.correctDefinition)    #debugging
                    
            for x, definition in enumerate(definitions):
                if definition.text == self.correctDefinition:
                    answerButtons[x].click()
                    #print("Definition matched at button " + choiceList[x])
                    self.currentCommand = vocabWord.text + ": definition matched at button " + choiceList[x]
            

            i += 1
            self.iterations += 1
            self.completedWords += 1
        
        
        
        
        # INSERT EMAIL TEACHER FUNCTION
        # If doesn't load, go to account and send details manually.
        # consider sending from account permanently rather than waiting on fetch
        # navigate to view results, send results
        send_results(browser, self.email)
        
        
        # BEGINNING OF CONCLUDING FUNCTIONS.
        self.currentOperation = "list completed"
        print_message("List completed. Instance finished")
        #   - potentially add preview of words in command output
        #   - provide email confirmation in command output
    
        
    # BEGINNING OF WEBSITE DEPENDENT (JQUERY) FUNCTIONS
    
    def get_creds_valid(self):
        return self.creds_valid


    def percent_done(self):
        #print(self.completedWords)
        return round(((self.completedWords / (self.list_length * 2)) * 100) , 1)
    
    def get_completed_words(self):
        return self.completedWords
    
    
    def get_current_word(self):
        return self.currentWord
    
    
    def get_correct_definition(self):
        return self.correctDefinition
    

    def get_current_operation(self):
        return self.currentOperation
    

    def get_command_output(self): #ADD REDUNDANCY SOLUTION (DON'T RETURN IF IT IS THE SAME AS LAST)
        return self.currentCommand
    
    
    def get_time_ellapsed(self):
        return round((self.ellapsedTime + (time.time() - self.initTime)), 2)
        


   

    

        


    


            
            
            
            
            

            
            
            
            
            
            
#solver = list_solver('https://www.vocabtest.com/definitions.php?grade=9&Unit=5', 'nlitz2468', 'mathew88', "heck")
#browser = webdriver.Chrome()
#browser.get('https://www.vocabtest.com/login.php')
#solver.login(browser, 'nlitz2468', 'mathew88')
# TESTING
            
            
            
            
            
            
            
            
            
            
            
            
            
            
    