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


while(True):
    pass

