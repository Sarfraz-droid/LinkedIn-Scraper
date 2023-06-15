from dotenv import load_dotenv
import pandas as pd

load_dotenv()

from runner import Runner

instance = Runner.get_instance()

instance.RUN()

instance.Login()

path = input("After login, enter your scrape excel file name")

print(f'Defining Data...')

instance.DefineData(path=path)

start = input('Press S to start');

if start == 'S':
    instance.startScrape()


while(True):
    pass

