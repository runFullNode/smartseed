from re import match
from smartseed.main.gentoolkit import GenToolkit

class EntropyGen(GenToolkit):
    """ base class for entropy generators """

    title = str()       # generator title
    descr = str()       # short description
    explain = str()     # full explaination

    entropy = str()     # provided/generated entropy
    user_input = str()  # usable entropy
    e_numbrrr = str()   # formatted entropy (ready to convert to binary)
    b_entropy = str()   # entropy converted to binary

    phrase_len = None
    min_length = None
    max_length = None

    provide_mirrors = True

    alpha2num = None

    seed_data = dict()
    
    indent = ' '*4

    def __init__(self, settings):
        self.phrase_len = settings.phrase_length
        self.min_length = settings.blen_min
        self.max_length = settings.blen_min
        self.alpha2num = settings.alpha2num
        self.showTitle()
        
        if self.explain: 
            self.extendExplanation()
            self.showExplanation()
        else: 
            self.showDescription()

    def run(self):
        pass

    def showTitle(self):
        line = f"{self.indent}{'-'*len(self.title)}"
        title = f"{self.indent}{self.title.upper()}"
        print(f"{line}\n{title}\n{line}")
    
    def extendExplanation(self):
        """ add extra text to explanation """
        e = "Any text containing non digits will be converted to digits."
        self.explain += f"\n{self.indent}{e}\n"

    def showExplanation(self):
        print(self.explain)
    
    def showDescription(self):
        print(f'{self.indent}{self.descr}')
    
    def getUserInput(self):
        pass

    def generate(self):
        pass
    
    def getEntropy(self):
        return self.entropy

    def getBinary(self):
        return self.b_entropy
    
    def convertAlpha2Num(self, abc_str):
        return self.alpha2num.convertString(abc_str)

    def digitToBinary(self, digit):
        """ convert even digits to 0 and odd ones to 1 """
        return str(int(digit) % 2)

    def processEntropy(self, entropy):
        """ format nondigits to digits """

        e_number = self.convertAlpha2Num(entropy.replace(' ', ''))
        b_entropy = ''.join([self.digitToBinary(dgt) for dgt in e_number])

        return e_number, b_entropy

    def showCheckError(self, user_input):
        print(f'\n{self.indent*2}"{user_input}" leads to duplicates in seed phrase.')
        print(f'{self.indent*2} please try somethinge else.')
