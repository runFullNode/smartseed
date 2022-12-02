from smartseed.main.gentoolkit import GenToolkit

class SeedViewer(GenToolkit):

    seed_obj = object()
    
    def __init__(self, seed_obj):
        self.seed_obj = seed_obj
    
    def revealAll(self):
        """ display final result """
        self.clearScreen()              # GenToolkit method
        self.showUserInput()
        self.showUsableEntropy()
        self.showNumberEntropy()
        self.showValidBinary()
        groups = self.prepareGroups()
        self.printGroups(groups)
        self.showSeedPhrase()
    
    def showUserInput(self):
        """ display user input """
        if self.seed_obj.user_input:
            print(f"** user input -> '{self.seed_obj.user_input}'")
    
    def showUsableEntropy(self):
        """ display usable entropy """
        if self.seed_obj.e_usable:
            print(f"** used chars -> '{self.seed_obj.e_usable}'")
    
    def showNumberEntropy(self):
        """ display entropy converted to numbers """
        if self.seed_obj.e_numbrrr:
            print(f"** generated  -> '{self.seed_obj.e_numbrrr}'")
    
    def showValidBinary(self):
        """ display valid entropy """
        if self.seed_obj.valid_bin:
            print(f"** to binary  -> '{self.seed_obj.valid_bin}'")
    
    def showSeedPhrase(self):
        """ display complete seedphrase """
        print(f"\n** seed phrase **\n", end='')
        self.printSeed(self.seed_obj.valid_bin)

    def prepareGroups(self):
        """ prepare groups for displaying """
        seed = self.seed_obj
        # group valid bin 
        valid_bin = self.groupString(seed.valid_bin)
        # group number entropy
        ent_num = self.groupString(seed.e_numbrrr)[:len(valid_bin)]
        # get wordlist index and associated word
        i, w = list(), list()
        for bin in valid_bin:
            i.append(self.binaryToInt(bin))
            w.append(self.binaryToWord(bin))
        
        o = self.prepareLastBins()

        return zip(ent_num, valid_bin, i, w, o)
        
    def prepareLastBins(self):

        heading = ' all options for last word:'
        warning = [ ' please note:', 
                    '   using a different last',
                    '   word would unlock a',
                    '   completely different',
                    '   set of wallets. ']
        if self.seed_obj.last_bins:
            o = ['','', heading ,'']
            lastword = self.seed_obj.valid_bin[-11:]
            for lastbin in self.seed_obj.last_bins:
                l = f'{"** " if lastbin == lastword else "   "}'
                l += f'{self.formatReadable(lastbin)} -> {self.binaryToWord(lastbin)}'
                o.append(l)
            o += ['', '']
            o += warning
            o += ['' for _ in range(len(self.seed_obj.valid_bin)-len(o))]
        else:
            o = ['' for _ in range(len(self.seed_obj.valid_bin))]
        return o

    def printGroups(self, groups):
        """ displays a screen with all information """
        
        i = 0
        div = '|'
        print()
        # display info line for line
        for chunk in groups:
            print(f'{str(i+1).rjust(2)}.', end=' ')
            print(f'{self.formatReadable(str(chunk[0])):<13}', end=f' {div} ')
            print(f'{self.formatReadable(str(chunk[1])):<13}', end=f' {div} ')
            print(f'{chunk[2]:>4}', end=f' {div} ')
            print(f'{chunk[3]:<9}', end='')
            print(f'{chunk[4]}')
            i += 1

    def printSeed(self, binary_string, short=False):
        """ Print complete seed phrase """
        bins = self.groupString(binary_string)
        for s in bins:
            w = self.binaryToWord(s)
            print(f'{w[:4] if short else w}', end=' ')
        print('\n')

    @staticmethod
    def binaryToInt(bin_str):
        """ Return integer value of binary string """
        return int(bin_str, 2)

    def binaryToWord(self, b):
        """ Return word from wordlist associated with binary"""
        return self.seed_obj.settings.wordslist[self.binaryToInt(b)]