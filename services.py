from Theme.Service import ThemeService as ThemeService
from enum import Enum
from multiprocessing import Process, Pipe

Service_Pipe, Return_Pipe  = Pipe()
Theme_Pipe, Theme_Return_Pipe = Pipe()

services = {}

class Services(Enum):
    Theme_Service = 1
    Settings_Service = 2

def Start_Services():
<<<<<<< HEAD
    # Start Theme Service

    theme_process = Process(target=ThemeService,args=(Theme_Pipe, Theme_Return_Pipe), daemon=True)
=======

    theme_service = ThemeService(Theme_Pipe, Theme_Return_Pipe)
    theme_process = Process(target=theme_service.run, daemon=True)
>>>>>>> b4f9613ef3de6b3e727d68554281b045283f5f3e
    theme_process.start()
    services[Services.Theme_Service] = theme_process


    return {
        Services.Theme_Service: (theme_process, Service_Pipe, Theme_Return_Pipe)
    }

def get_Pipes():
    return Service_Pipe, Return_Pipe

def get_Theme_Pipes():
    return Theme_Pipe, Theme_Return_Pipe
