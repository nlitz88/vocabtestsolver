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
        opts.binary_location = chrome_bin
        self.browser = webdriver.Chrome(executable_path="chromedriver", chrome_options=opts)
        """

        options = ChromeOptions()
        options.add_argument("--headless")
        #options.add_experimental_option("detach", True)
        self.browser = webdriver.Chrome(chrome_options=options)
        
        Thread.__init__(self)
    
    
    def run(self):
        
        
        # BEGINNING OF PROCESS DEPENDENT VARIABLES
        
        
        choiceList = ['a', 'b', 'c', 'd', 'e']  # CORRESPONDING SENDABLE KEY VALUES
        timeThreshold = 20  # Wating threshold for WebDriverWait
        loginLink = 'https://www.vocabtest.com/login.php'
        accountLink = 'https://www.vocabtest.com/user_tests_completed.php'


        # CEATE REFERENCE TO CHROME INSTANCE
        #   - use browser from instance in usable format
        browser = self.browser
        browser.implicitly_wait(10)
        

        
        
        # BEGINNING EXTERNAL LEARNING/SOLVING FUNCTIONS
        
        def get_list_length(browser):
            
            self.currentOperation = "getting list length"
            indicator = browser.find_element_by_id('questionNum')
            length = indicator.text
            num, length = length.split('/')
            self.list_length = int(length)
        

        # could be imported from list_validator; this was quick solution
        def get_list_type(browser):
            
            url = browser.current_url

            acceptedLists = ["definitions", "sentences", "reverseDefinitions", "reverseSentences", "synonyms", "reverseSynonyms", "antonyms", "reverseAntonyms"]
            for types in acceptedLists:
                if types in url:
                    self.listType = types
                    break


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
                return False
                

        def login_status(browser):

            def destination_valid(browser):
                indicator = browser.find_element_by_xpath('//*[@id="header"]/tbody/tr/td[3]/a[2]')
                if indicator.text == 'Log Out':
                    #print('creds valid')
                    return True
                else:
                    #print('creds invalid')
                    return False

            try:
                loggedIn = WebDriverWait(browser, 5).until(destination_valid)
            except:
                loggedIn = False
            
            return loggedIn

                         
        def send_results(browser, email):
            
            #webdriverwait not needed due to implicit wait; being reused
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
        

        def save_list(browser):
            saveButton = browser.find_element_by_id('saveButton')
            saveButton.click()


        # Loads completed tests page, but also checks to ensure that correct list is sent
        def view_results(browser):
            
            completedLists = browser.find_element_by_xpath('//*[@id="contentHolder"]/div/div[1]')
            completedListLinks = completedLists.find_elements_by_tag_name('a')
            completedListNames = completedLists.find_elements_by_tag_name('sup')

            for x, names in enumerate(completedListNames):

                nameArr = names.text.split(' -- ')
                name = list(nameArr[0])
                name[0] = name[0].lower()
                if " " in name:
                    name[name.index(" ")] = ""
                name = "".join(name)

                if name == self.listType:
                    # steps 3 to find respective link
                    if x == 0:
                        linkIndex = 0
                    else:
                        linkIndex = x + 3

                    if completedListLinks[x].text == "View Results":
                        completedListLinks[x].click()
                        break

    
        def elimCSS(browser):
            page = browser.find_element_by_tag_name('body')
            browser.execute_script("document.head.parentNode.removeChild(document.head);", page)


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
        ONLY USE IF BROWSER HAS FAILED X AMOUNT OF TIMES. ADD FAILCOUNT
        IN CASE DRIVER BECOMES ABSOLUTELY UNRESPONSIVE
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
    
        
        # FINDS RESPECTIVE DEFINITION TO CURRENT WORD AND CLICKS RESPECTIVE ANSWERBUTTON
        def match_definition(vocabWord, definitions, answerButtons):

            for word in self.word_list:
                if word == vocabWord.text:
                    self.correctDefinition = self.word_list[word]
                    #print(self.correctDefinition)    #debugging
                    
            for x, definition in enumerate(definitions):
                if definition.text == self.correctDefinition:
                    answerButtons[x].click()
                    #print("Definition matched at button " + choiceList[x])
                    self.currentCommand = vocabWord.text + ": definition matched at button " + choiceList[x]

    
    
        # NAVIGATE TO LIST
        browser.get(self.link)
        elimCSS(browser)    #decreases loadingtimes
        get_list_length(browser)
        get_list_type(browser)
        #print(self.list_length)
        


        
        # BEGINNING OF PROCESS (LEARNING LIST)
        #   - put into TRY / EXCEPT format to handle errors

        while(len(self.word_list) < self.list_length):
            
            self.currentOperation = "learning list"
            #print_message("Iterations: " + str(self.iterations))
            
            try:
                vocabWord = WebDriverWait(browser, timeThreshold).until(word_loaded)
                definitions = WebDriverWait(browser, timeThreshold).until(definitions_loaded)
                answerButtons = WebDriverWait(browser, timeThreshold).until(answerButtons_loaded)
            except:
                # REFRESH PAGE IN ORDER TO RELOAD UNRESPONSIVE ELEMENTS
                print_message("Elements not loaded, reloading page")
                self.currentCommand = "Reloading page, elements failed to load"
                
                browser.refresh()
                elimCSS(browser)

                self.iterations = 1
                continue


            # IF WORD IS KNOWN, ANSWER QUESTIONS CORRECTLY TO SAVE TIME
            if is_duplicate(vocabWord.text):
                match_definition(vocabWord, definitions, answerButtons)
                self.currentCommand = (vocabWord.text).upper() + ": duplicate, already found"

            
            found = False
            for x, button in enumerate(answerButtons):
                
                button.click()
                time.sleep(.2)
                
                if button.text == '✓':
                    self.correctDefinition = definitions[x].text
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
            #print_message("Iterations: " + str(self.iterations) + " | Loop: " + str(i))

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
                elimCSS(browser)

                continue
                
            
            match_definition(vocabWord, definitions, answerButtons)
            

            i += 1
            self.iterations += 1
            self.completedWords += 1
        
        
        
        
        # INSERT EMAIL TEACHER FUNCTION
        
        time.sleep(2)       #lazy wait for the page to fetch the reults. Should replace with

        browser.get(accountLink)
        print_message(browser.current_url)

        # redundant but functional
        if not login_status(browser):
            print_message("Not logged in, logging in again")
            self.loggedIn = login(browser, self.username, self.password)
            while not self.loggedIn:
                loggedIn = login(browser, self.username, self.password)

        view_results(browser)
        send_results(browser, self.email)
        
        
        # BEGINNING OF CONCLUDING FUNCTIONS.
        self.currentOperation = "list completed"
        print_message("List completed. Instance finished")
        # exits individual chrome instance. Subject to change
        browser.quit()
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
            
            
            
            
            
            
            
            
            
            
            
            
            
            
    