import sys
from smartseed.wordlists.wordlists import WordsList
from smartseed.ui.splash import Splash
from smartseed.ui.get_input import ChoiceInput, BoolChoice
from smartseed.alpha2num.alpha2num import Alpha2Num
from smartseed.alpha2num.a2n_dicts import a2n_deutsch, a2n_123

class Settings:

    # wordslist settings
    wordslist_language = 'english'
    default_language = 'english'
    wordslist = tuple()

    # seed settings
    default_p_len = 24
    phrase_length = 24
    default_mirrors = False
    enable_mirrors = False

    # alpha2num dictionary
    confirm_a2n = False
    abc2n_dict = a2n_deutsch()
    num2n_dict = a2n_123()
    
    alpha2num = None

    # ui settings
    splash = Splash(top_msg='setting up', btm_msg=' ')

    def __init__(self, reset=False):
        """ initiate settings """
        self.processCommands()
        if reset: self.resetSettings()
        self.setup()
    
    def processCommands(self):
        if '--setup' in sys.argv: self.resetSettings()
        else:
            if '--set_length' in sys.argv:  self.phrase_length = None
            if '--set_mirrors' in sys.argv: self.enable_mirrors = None
            if '--set_language' in sys.argv:    self.wordslist_language = None
            if '--set_a2n' in sys.argv:     self.confirm_a2n = True

    def setup(self):
        """ set all settings """
        # setup and load wordslist
        self.wordslist = self.setWordslist()
        # setup phrase length
        if not self.phrase_length:
            self.setPhraseLength()
        # set min and max needed to hash valid binary
        self.setBitLengths()
        # setup mirror_option
        if self.enable_mirrors == None:
            self.enable_mirrors = self.setMirrors()
        self.alpha2num = Alpha2Num(settings=self, confirm_setup=self.confirm_a2n)

    def showSplash(self):
        self.splash.showSplash()

    def setWordslist(self):
        """ setup and load wordslist """
        self.showSplash()
        wordslist = WordsList(wordslist_language=self.wordslist_language,
                              default_language=self.default_language)
        return wordslist.loadWordlist()

    def setPhraseLength(self):
        """ prompt user set phrase length to 12 or 24 """
        request = f"please specify seed phrase length"
        choices = (12, 24)
        default = self.default_p_len
        c_input  = ChoiceInput(request=request, default=default, choices=choices, splash=self.showSplash)
        self.phrase_length = int(c_input.getResponse())

    def setBitLengths(self):
        """ Set string length needed to get valid binary for phrase length """
        try:
            # set binary min and max lengths
            self.blen_min = int(128 * self.phrase_length / 12)
            self.blen_max = int(132 * self.phrase_length / 12)
        except TypeError:
            # set phrase length if error occured
            self.setPhraseLength()
            # set bit lengths again
            self.setBitLengths()

    def setMirrors(self):
        """ prompt user to enable seed mirrors"""
        request = f"would you like to enable seed mirrors?"
        return BoolChoice(request=request, default=self.default_mirrors, splash=self.showSplash).getResponse()

    def resetSettings(self):
        """ reset settings to default """
        self.wordslist_language = str()
        self.default_language = 'english'
        self.wordslist = tuple()
        self.phrase_length = None
        self.confirm_a2n = True
        self.enable_mirrors = None
        if self.alpha2num:
            self.abc2n_dict = self.alpha2num.abc2n_dict
            self.num2n_dict = self.alpha2num.num2n_dict