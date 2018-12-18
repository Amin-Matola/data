#---------------------------Log in on any site with python: selenium ----------------------------
# 1: enter the location url to of your site
# 2: enter the name of target thing to be scraped
# 3: enter the css_selector to select the target
# 4: get the results

#: Pull off the trigger
#--------------------------- Last Modified By : Amin Matola -------------------------------------

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class Pylog:
    """ Module for signing in to website using python """
    
    def __init__(self,url,username,password):
        self.url    = url
        self.user   = username
        self.passwd = password
        self.browser= webdriver.Firefox('/path/to/firefoxdriver.exe')     # or null for automatic search
        
    # We will be using our above firefox webdriver for this code
    
    def get_source(self):
        if len(self.url):                                                 # check if  user entered location website
           self.browser.get(self.url)                                     # open connection to the website provided
           time.sleep(2)                                                  # wait two sec. before dishing another burden
              
        else:
           self.url  = input("Hey! you forgot URL, enter one please")     # Humbly Ask s/he to enter Location
           self.get_source()                                              # repeat the process again with location now entered
        self.process_source_code()                                        # now the code processor should enter the doc
        
    def process_source_code(self):
           self.username = self.browser.find_element_by_name('username')   # getting username input field...
           self.username.send_keys(self.user)                             # fill the username field like pressing on keyboard
           time.sleep(0.5)                                                # wait 3 milliseconds
           self.password = self.browser.find_element_by_name('password')  # getting password input field...
           self.password.send_keys(self.passwd)
           time.sleep(0.5)
           self.log_butn = self.browser.find_element_by_xpath('//[@type='submit'])   # getting submit input field...
               
           self.login()
           
    def login(self):
             try:
                self.log_btn.click()
             except Exception as e:
                return 'Sign In Unsuccessful!\n\n%s'%e
             return "You are signed in now, %s! All the best."%self.user
                
             
            
           
           
           
