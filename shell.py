from rich import print as rprint
from rich.console import Console
from runner import Runner


options = [
    '[1] : Start Session',
    '[2] : Verify LinkedIn & Find Emails',
    '[3] : Scan Through CSV and Verify'
]

console = Console()

class SHELL:
    __instance = None
    
    @staticmethod
    def get_instance():
        if SHELL.__instance == None:
            SHELL()
        return SHELL.__instance

    def __init__(self):
        """ Virtually private constructor. """
        self.runner = Runner.get_instance()
        if SHELL.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            SHELL.__instance = self

    def Repeat(self):
        self.Input()
        pass

    def startSession(self):
        
        self.Input()
        self.Repeat()
        pass
    
    def InitSession(self):
        print("Init Session")
    
        self.runner.RUN()        
        self.runner.Login()
        self.Repeat()
        pass
    
    def VerifyLinkedInID(self):
        
        link = console.input(prompt=f'Enter Linkedin Link')
        company = console.input(prompt=f'Enter Company Name')
        name = console.input(prompt=f'Enter your name')
        
        self.runner.scapeLink(company=company,name=name, link=link)
        pass
    
    def ScanCSV(self):
        path = console.input(prompt=f'Enter File Path')
        
        self.runner.DefineData(path=path)
        self.runner.startScrape()
        
        pass

    def Input(self):
        
        logo = '''
 _      _       _            _ _____          _____                                
| |    (_)     | |          | |_   _|        / ____|                               
| |     _ _ __ | | _____  __| | | |  _ __   | (___   ___ _ __ __ _ _ __   ___ _ __ 
| |    | | '_ \| |/ / _ \/ _` | | | | '_ \   \___ \ / __| '__/ _` | '_ \ / _ \ '__|
| |____| | | | |   <  __/ (_| |_| |_| | | |  ____) | (__| | | (_| | |_) |  __/ |   
|______|_|_| |_|_|\_\___|\__,_|_____|_| |_| |_____/ \___|_|  \__,_| .__/ \___|_|   
                                                                  | |              
                                                                  |_|                     
        '''
        print(logo)
        
        rprint('\n'.join(options))
        
        value = int(console.input(prompt=f'Enter your input [1-{len(options)}] : '))
        
        rprint(f'Chosen value is {value}')
        
        match value:
            case 1:
                print('Value')
                self.InitSession()              
                pass

            case 2: 
                self.VerifyLinkedInID()
                pass
            
            case 3: 
                self.ScanCSV()
                pass    
    
            case _:
                pass
        

        pass
    