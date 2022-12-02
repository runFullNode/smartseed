#!/usr/bin/env python3

from os import system
from smartseed.main.settings import Settings
from smartseed.ui.entropymenu import EntropyMenu
from smartseed.main.seedobj import SmartSeed
from smartseed.ui.userinterface import UserInterface

class runApp():

    def __init__(self, settings=None):
        # initiate UserInterface
        ui = UserInterface()
        # initiate settings
        if not settings: settings = Settings()
        ui.showSplash()
        # select entropy creation app
        entropyApp = EntropyMenu().getSelectedApp()
        if entropyApp == 'settings':
            settings.resetSettings()
            settings.setup()
            return runApp(settings)
        if entropyApp == 'quit': ui.exitApp()
        system('clear')
        entropyApp(settings)
        system('clear')
        # initiate seed 
        seed = SmartSeed(settings, entropyApp.seed_data)
        seed.getValidBinary()
        seed.getLastBins()
        seed.showFinalResult()
        # get seed mirrors
        if settings.enable_mirrors and entropyApp.provide_mirrors:
            if ui.confirmShowMirrors():
                mirrors = seed.getMirrors()
                for mirror in mirrors.values():
                    mirror.showFinalResult()
                    input('\npress return to continue...')
        else:
            input('\npress return to continue...')
        return runApp(settings)

if __name__ == '__main__':
    runApp()