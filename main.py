from dotenv import load_dotenv
import pandas as pd
from rich import pretty

pretty.install()
load_dotenv()

from runner import Runner
from shell import SHELL

instance = Runner.get_instance()

shellInstance = SHELL.get_instance()

shellInstance.startSession()

# instance.RUN()

# instance.Login()

# path = input("After login, enter your scrape excel file name")

# print(f'Defining Data...')

# instance.DefineData(path=path)

# start = input('Press S to start');

# if start == 'S':
#     instance.startScrape()


while(True):
    pass

