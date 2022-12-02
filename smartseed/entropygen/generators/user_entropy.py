from smartseed.entropygen.entropygen import EntropyGen
from os import system

class UserEntropy(EntropyGen):

    title = 'user-defined'
    descr = 'user enters entropy'
    explain = """
    Type or paste any text to convert to entropy. Characters will be
    converted using the current alpha2num setup. Entering less than
    the required amount of characters, will display current progress.
    
    After entering the sufficient amount of characters, s seed phrase
    will be calculated. 
    """

    def __init__(self, settings):
        super().__init__(settings)
        self.run()

    def run(self):
        u, n, b = self.getUserInput()
        self.seed_data['user_input'] = u
        self.seed_data['e_numbrrr'] = n
        self.seed_data['b_entropy'] = b

    def getUserInput(self):
        """ Get entropy from user input """
        user_input = str()  # user input
        e_usable = str()    # used user input
        e_number = str()   # formatted to digits
        e_binary = str()    # b_entropy
        while self.max_length >= len(e_number) < self.min_length:
            # calculate amount of chars needed to complete string
            chars_needed = self.min_length - len(e_number)
            # prepare request text
            request = f'\n{self.indent}Please enter text/entropy; '
            request += f'\n{self.indent}({chars_needed} characters still needed): '
            # get response for user
            response = input(request)
            # convert response to entropy
            usable, number, binary = self.processEntropy(response)
            # extend entropy with newly converted strings 
            user_input += f"{response.strip()} "
            e_usable += usable      
            e_number += number    
            e_binary += binary
            # show current progress
            self.showProgress(user_input, (e_usable, e_number, e_binary))
        return user_input, e_number[:self.min_length], e_binary[:self.max_length]

    def processEntropy(self, entropy):
        """ format nondigits to digits """

        e_usable = str()
        e_number = str()
        b_entropy = str()
        
        for chr in entropy.replace(' ', ''):
            dgt = self.convertAlpha2Num(chr)
            if dgt: e_usable += f"{chr}{'*'*(len(dgt)-1)}"
            e_number += str(dgt)
            for d in str(dgt):
                b_entropy += self.digitToBinary(d)
        return e_usable, e_number, b_entropy

    def showProgress(self, user_input, *data):
        """ print a screen showing progress of converted entropy """
        system('clear')
        print(f'\nentered entropy: {user_input}\n')
        self.printChunks(*data, self.phrase_len)
