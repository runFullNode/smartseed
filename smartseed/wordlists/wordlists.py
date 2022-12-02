import os
try:
    import requests
except ModuleNotFoundError as e:
    print(e)

from smartseed.ui.get_input import menuChoice

class WordsList:

# path settings
    wordlists_dir = 'bip-0039'
    wordlists_path = os.path.join(os.path.dirname(__file__), wordlists_dir)
    wordlists_url = 'https://raw.githubusercontent.com/bitcoin/bips/master/bip-0039/'

# bip-39 language settings
    languages = tuple()
    lang_pref = str()

    def __init__(self, wordslist_language=None, default_language=None):
        """ Initiate configuration """
        # create a tuple of available languages
        self.getWordlists()
        self.languages = self.getLanguages()
        self.default_lang = default_language
        
        if wordslist_language not in self.languages:
            self.setLanguage()
        else:
             self.lang_pref = wordslist_language
            
    def getLanguages(self):
        """ return a tuple of available languages in directory """
        languages = list()
        for file in os.listdir(self.wordlists_path):
            if file.endswith('.txt'):
                languages.append(file.split('.')[0])
        return tuple(sorted(languages))

    def setLanguage(self):
        heading = f'please specify a prefered bip-39 wordslist language'
        choices = self.getLanguages()
        request = f"what's it gonna be, pleb?"
        response = menuChoice(heading=heading,
                              choices=choices,
                              request=request,
                              default=self.default_lang).getResponse()
        self.lang_pref = self.languages[response-1]
        print(f'bip39 language set to {self.lang_pref}\n') if self.lang_pref == self.default_lang else None

    def loadWordlist(self):
        """ Return a tuple from official bip-39 wordlist """
        filename = os.path.join(self.wordlists_path, f'{self.lang_pref}.txt') 
        words = list()
        with open(filename, 'r') as f:
            for w in f.readlines():
                words.append(w[:-1])
        return tuple(words)

    # downloading functions, only works if requests available
    def getWordlists(self):
        if not self.wordlistsDirectoryExist():
            self.createWordlistsDirectory()
            self.downloadWordlists()

    def wordlistsDirectoryExist(self):
        """ check whether wordslist directories exist """
        # print('checking for local wordlists directory', end=' ')
        return bool(os.path.isdir(self.wordlists_path))

    def createWordlistsDirectory(self):
        """ Create a local directory if none exists """
        if not self.wordlistsDirectoryExist():
            print(f'\n\tcreating directory at\n\t{self.wordlists_path}')
            os.makedirs(self.wordlists_path) # create directory

    def downloadWordlists(self):
        """ Download wordlists if necessary """
        languages = ('czech','english','french',
                     'italian','portuguese','spanish')
        for lang in languages:
            filename = f'{lang}.txt'
            file_path = os.path.join(self.wordlists_path, filename)
            if not os.path.isfile(file_path):           # check if file exists
                print(f'\tdownloading {filename}', end=' ')
                url = f'{self.wordlists_url}{filename}'
                wordlist = requests.get(url)            # download file
                with open(f'{file_path}', 'wb') as local_copy:
                    local_copy.write(wordlist.content)  # write downloaded file to disk
                    print('...done'.rjust(25 - len(filename)))