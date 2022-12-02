import inspect
import os

from smartseed.entropygen.generators import *
from smartseed.ui.get_input import menuChoice

class EntropyMenu:

    apps = tuple()

    def __init__(self):
        self.apps = self.getApps()

    def getUserInput(self):
        h = 'please choose method to generate entropy'
        c = self.menuChoices()
        r = 'pick yer poison, pleb'
        
        return menuChoice(heading=h, choices=c, request=r).getResponse()

    def getSelectedApp(self):
        selection = self.getUserInput() - 1
        try:
            return self.apps[selection]
        except IndexError:
            return self.menuChoices()[selection]

    def getApps(self):
        """ return a tuple of classes from entropygenerator modules """
        gens_path = os.path.join(os.path.dirname(__file__), os.pardir,
                                'entropygen', 'generators')
        modules = [file[:-3] for file in os.listdir(gens_path)
                  if file.endswith('.py') and not file.startswith('__')]

        classes = list()
        for mod in sorted(modules):
            imports = inspect.getmembers(eval(mod), inspect.isclass)
            for i in imports:
                if i[1].__module__ == f'smartseed.entropygen.generators.{mod}':
                    classes.append(i[1])
        
        return classes
    
    def menuChoices(self):
        return [gen.title for gen in self.apps] + ['settings', 'quit']