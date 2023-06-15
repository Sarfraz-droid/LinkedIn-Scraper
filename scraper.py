from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

class ScraperService:
    
    @staticmethod
    def ScrapeID(driver: webdriver.Chrome, companyName: str, Name: str):
        try:
            print(f'Current URL : {driver.current_url}')
            el = WebDriverWait(driver, timeout=5).until(lambda d : d.find_element(By.CLASS_NAME,'pv-text-details__left-panel') )
            text = str(el.text).lower()
            name = str(Name).lower()
            if name in text:
                print(f'Valid!')
                return True
            return False
        except:
            print("Error Occurred")
            return False