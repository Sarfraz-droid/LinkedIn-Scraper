from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from dotenv import dotenv_values
from selenium.webdriver.common.by import By
import numpy as np
import pandas as pd
from scraper import ScraperService

config = dotenv_values(".env")


class Runner:
    __instance = None
    
    @staticmethod
    def get_instance():
        if Runner.__instance == None:
            Runner()
        return Runner.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if Runner.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Runner.__instance = self


    def RUN(self):
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-extensions')
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get('https://google.com')

    def Login(self):
        self.driver.get('https://www.linkedin.com')
        self.driver.implicitly_wait(3)
        
        username = self.driver.find_element(By.ID,'session_key')
        username.send_keys(config['USERNAME'])

        # sleep for 0.5 seconds
        time.sleep(0.5)

        # locate password form by_class_name
        password = self.driver.find_element(By.ID,'session_password')

        # send_keys() to simulate key strokes
        password.send_keys(config['PASSWORD'])
        time.sleep(0.5)

        # locate submit button by_xpath
        sign_in_button = self.driver.find_element(By.XPATH,'//*[@type="submit"]')

        # .click() to mimic button click
        sign_in_button.submit()
        time.sleep(1)

    def DefineData(self,path):
        self.path = path
        self.df = pd.read_csv(self.path)
        self.data = self.df.to_numpy()
        # self.data = np.delete(self.data,0,axis=0)
        self.columns = self.df.columns.values
        
        cl= list(self.df.columns.values)

        for i in range(0,len(cl)):
            cl[i] = f'Index {i} - {cl[i]}'

        
        print('\n'.join(cl))
        
        self.linkedInPos = int(input("Choose Linkedin Index : "))  
        
        self.CompanyPos = int(input("Choose Company Index : "))
        
        self.NamePos = int(input("Choose Name Index : "))

    def startScrape(self):
        print(len(self.data))
        print(self.data[0])
        self.falseList = []
        for info in self.data:
            print(f'Starting scrape with {info[self.linkedInPos]} - {info[self.CompanyPos]} - {info[self.NamePos]}')
            self.driver.get(info[self.linkedInPos])
            self.driver.implicitly_wait(2)
            status = ScraperService.ScrapeID(driver=self.driver, companyName=info[self.CompanyPos], Name=info[self.NamePos])
            if status == False:
                self.falseList.append(info.tolist())
                
                
        print('Completed Scrape, Storing to Sheet')
        print(self.falseList)
        df2 = pd.DataFrame(self.falseList, columns=self.columns)
        df2.to_csv('falseList.csv')
        
        print('Stored Data!')
        
    
    def scapeLink(self, link, name, company):
        self.driver.get(link)
        self.driver.implicitly_wait(2)
        status = ScraperService.ScrapeID(driver=self.driver, companyName=company, Name=name)
        
        if status == False:
            self.falseList.append({
                'link': link,
                'name' : name,
                'company' : company
            })
        pass
        
        