from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import pandas as pd
from rich import print as rprint
from console import console
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

class ScraperService:
    
    @staticmethod
    def ScrapeID(driver: webdriver.Chrome, companyName: str, Name: str):
        try:
            WebDriverWait(driver, timeout=15).until(lambda d : d.find_element(By.CLASS_NAME,'pvs-list') or d.find_element(By.CLASS_NAME,'not-found__container') )
            
            name = str(Name).lower()
            html = driver.page_source
            
            soup = BeautifulSoup(html,'html.parser')
            
            
            if 'This page doesn’t exist' in soup.text:
                console.print(f'[red]Invalid Linkedin URL[/red]')
                return False
            

            companyName = str(companyName).lower()            
            el = soup.find('div','pv-text-details__left-panel').find('h1','text-heading-xlarge')   
         
            name_ratio = fuzz.ratio(el.text.lower(),name);    
            
            if name_ratio < 70:
                console.print('[red] Name is invalid[/red]')
                return False
            
            
            
            
            verified_link = False
            
            for ul in driver.find_elements(By.CLASS_NAME,'pvs-list'):
                try:
                    for exp in ul.find_elements(By.CLASS_NAME,'pvs-list__item--one-column'):
                        _text = exp.text.lower()
                        console.print(_text)
                        
                        if companyName in _text and 'present' in _text:
                            verified_link = True
                            break
                    
                    if verified_link:
                        break
                except:
                    pass
                
            if verified_link is False:
                console.print('[red]Company is invalid[/red]')
                
            return verified_link
        except:
            console.print("[red]Error Occurred[/red]")
            return False
    
    def storeCSV(data: list, columns: list, path: str) -> None:
        try:
            console.print(f'[italic]Exporting Invalid Data List....[/italic] as {path}')
            df = pd.DataFrame(data, columns=columns)        
            df.to_csv(path)

            console.print(f'[green]Exported False Data List Successfully at {path}![/green]')
        except:
            console.print('[red]Exporting Data Failed[/red]')
        
        pass