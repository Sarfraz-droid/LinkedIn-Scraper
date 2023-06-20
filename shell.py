from rich import print as rprint
from rich.console import Console
from runner import Runner


options = [
    '[1] : Start Session',
    '[2] : Verify LinkedIn & Find Emails',
    '[3] : Scan Through CSV and Verify',
    '[4] : Export InValid Data'
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
        restart = console.input(prompt="Do you want to restart?[Y/N]").lower()
        if restart == 'y':
            self.Input()
        else:
            exit()
        pass

    def startSession(self):
        
        self.Input()
        self.Repeat()
        pass
    
    def InitSession(self):
        rprint('\n\nOpening Selenium...')    
        self.runner.RUN()        
        rprint('\n\nLogging In')
        self.runner.Login()
        
        self.Repeat()
        pass
    
    def VerifyLinkedInID(self):
        [link,company,name] = self.runner.defineSingleData()
        
        self.runner.scrapeLink(company=company,name=name, link=link)
        pass
    
    def ScanCSV(self):        
        self.runner.defineCSVData()
        self.runner.startScrape()
        
        self.Repeat()
        
        pass
    
    def ExportData(self):
        self.runner.exportData()
        
        self.Repeat()
        pass

    def Input(self):
        console.clear()
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
                self.InitSession()              
                pass

            case 2: 
                self.VerifyLinkedInID()
                pass
            
            case 3: 
                self.ScanCSV()
                pass   
        
            case 4:
                self.ExportData()
    
            case _:
                pass
        

        pass
    