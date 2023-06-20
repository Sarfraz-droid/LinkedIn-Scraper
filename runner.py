from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from dotenv import dotenv_values
from selenium.webdriver.common.by import By
import numpy as np
import pandas as pd
from scraper import ScraperService
from pathlib import Path
from rich.console import Console
import datetime

config = dotenv_values(".env")

console = Console()


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
            self.falseList = []
            Runner.__instance = self


    def RUN(self):
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-extensions')
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get('https://google.com')

    def Login(self):
        self.driver.get('https://www.linkedin.com/authwall')
        self.driver.implicitly_wait(5)
        try:
            toggleElement = self.driver.find_element(By.CLASS_NAME,'form-toggle')
            
            if toggleElement is not None and "Sign in" in toggleElement.text:
                toggleElement.click();
        except TimeoutError:
            print('.form-toggle tag not found')
        
        username = self.driver.find_element(By.ID,'session_key')
        time.sleep(0.5)
        username.send_keys(config['USERNAME'])

        # sleep for 0.5 seconds
        time.sleep(0.5)

        # locate password form by_class_name
        password = self.driver.find_element(By.ID,'session_password')
        

        # send_keys() to simulate key strokes
        password.send_keys(config['PASSWORD'])
        time.sleep(0.5)

        # locate submit button by_xpath
        sign_in_button = self.driver.find_element(By.XPATH,'//*[@data-id="sign-in-form__submit-btn"]')

        # .click() to mimic button click
        sign_in_button.submit()
        time.sleep(1)
        
    def defineSingleData(self):
        link = console.input(prompt=f'Enter Linkedin Link : ')
        company = console.input(prompt=f'Enter Company Name : ')
        name = console.input(prompt=f'Enter your name')
        
        return link, company,name


    def defineCSVData(self):
        console.print('[bold]NOTE : your file path must be relative to the [italic]assets/[/italic] folder[/bold]')
        _path = console.input('Enter your File Name: ')
        self.path = Path(f'./assets/{_path}')
        self.df = pd.read_csv(self.path)
        self.data = self.df.to_numpy()
        # self.data = np.delete(self.data,0,axis=0)
        self.columns = self.df.columns.values.tolist()
        
        cl= list(self.df.columns.values)

        for i in range(0,len(cl)):
            cl[i] = f'[bold]Index {i}[/bold] - {cl[i]}'
            
        console.print('\n'.join(cl))    
        
        self.linkedinPos = int(console.input("Choose Linkedin Index : "))          
        self.companyPos = int(console.input("Choose Company Index : "))        
        self.namePos = int(console.input("Choose Name Index : "))

    def startScrape(self):
        self.falseList = []
        for info in self.data:
            console.print(f'Checking for [link]{info[self.linkedinPos]}[/link] - [green]{info[self.companyPos]}[/green] - {info[self.namePos]}')            
            self.scrapeLink(link=info[self.linkedinPos], company=info[self.companyPos], name=info[self.namePos])

        export = console.input('Do you want to export the false data?[Y/N]').lower()
        
        if export == 'y':
            self.exportData()
        
        print('Stored Data!')
        
    def exportData(self):
        ScraperService.storeCSV(self.falseList, ['LinkedIn','Name','Company'], Path(f'./out/false_list_{datetime.datetime.now().strftime("%m_%d_%Y_%H_%M_%S")}.csv'))
    
    def scrapeLink(self, link, name, company):
        try:
        # if True:
            self.driver.get(link)
            self.driver.implicitly_wait(6)
            status = ScraperService.ScrapeID(driver=self.driver, companyName=company, Name=name)
            
            if status == False:
                self.falseList.append([link,name,company])
            pass
        except:
            console.print('[bold red] Invalid Link[/bold red]')
            self.falseList.append([link,name,company])
            pass
        
        