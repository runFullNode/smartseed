from smartseed.main.gentoolkit import GenToolkit
from smartseed.ui.splash import Splash, ExitSplash
from smartseed.ui.get_input import BoolChoice

class UserInterface(GenToolkit):

    splash = None
    exit_splash = None

    wordslist = tuple()

    def __init__(self):
        self.splash = Splash()
        self.exit_splash = ExitSplash()

    def showSplash(self):
        self.splash.showSplash()
   
    def confirmShowMirrors(self):
        request = '\nshow mirrored seed phrases?'
        return BoolChoice(request, default='y', no_indent=True).getResponse()
    
    def exitApp(self):
        self.exit_splash.showSplash()
        exit()