from re import match
from smartseed.ui.get_input import BoolChoice, UserInput

class Alpha2Num:
    """ classs to convert characters to digits """

    default_a = 1           # default number associated with letter 'a'
    default_i = 1           # increment between letters
    
    abc2n_dict = dict()     # dict - chars: associated numbers
    num2n_dict = dict()
    
    setup_complete = dict()
    
    skipped = list()        # list of skipped characters

    def __init__(self, settings, confirm_setup=False):
        self.setup_complete = {'letters': False,
                               'numbers': False}
        self.splash = settings.splash.showSplash
        self.abc2n_dict = settings.abc2n_dict
        self.num2n_dict = settings.num2n_dict
        if confirm_setup: 
            self.setup()
                    
    def setup(self, dict_type=None):
        if dict_type:
            if not self.setup_complete[dict_type]:
                if not self.confirmSetup(dict_type):
                    if dict_type == 'letters': self.setupAlphaDict()
                    if dict_type == 'numbers': self.setupNumDict()
                self.setup_complete[dict_type] = True
        else:
            for dict_type in (self.setup_complete):
                if not self.setup_complete[dict_type]:
                    self.setup(dict_type)

    def confirmSetup(self, dict_type):
        """ return user confirmation of current setup """
        self.splash()
        # print heading
        heading = f"confirm current alpha2num setup for {dict_type}:\n"
        print(f"{BoolChoice.indent[0]}{heading}")
        # show current setup
        self.showSetup(dict_type)
        # return user confirmation
        response = BoolChoice(f'are these conversions correct?', default='y').getResponse()
        print()
        return response

    def showSetup(self, dict_type):
        """ display current conversion setup """
        ind = BoolChoice.indent[1]      # indentation

        if dict_type == 'letters':
            a2n = self.getAlphaDict()
            a2n_dict = self.abc2n_dict
            sec = int(len(a2n)/3)
        
        elif dict_type == 'numbers':
            a2n = self.getNumsDict()
            a2n_dict = self.num2n_dict
            sec = int(len(a2n)/2)

        # print three columns with characters and associated numbers
        for i in range(sec):
            try:
                print(f"{ind}{a2n[i]}: {a2n_dict[a2n[i]]:<15}", end='')
            except IndexError:
                print()
            try:
                print(f"{a2n[i+sec]}: {a2n_dict[a2n[i+sec]]:<15}", end='')
            except IndexError:
                print()
            try:
                print(f"{a2n[i+sec*2]}: {a2n_dict[a2n[i+sec*2]]}")
            except IndexError:
                print()
        print()
   
    def setupAlphaDict(self, a=int(), b=int()):
        """ update and set Alpha2Num dict """
        
        request = f"give a number value for "
        
        if not a: a = UserInput(request=request+'a',
                        default=self.default_a, response_type=int).getResponse()
        if not b: b = UserInput(request=request+'b', 
                        default=a*2, response_type=int).getResponse()
        print()
        if a == b: return self.setupAlphaDict()
        # new empty a2n dict
        alpha = dict()

        # get old a2n dictionary
        old_a2n = self.getAlphaDict()

        # set number for a and increments to next numbers
        strt, incr = a, b-a
        # set counter, mulltiplier
        m = 0

        # create new a2n dict
        for char in old_a2n:
            alpha[char] = strt+m*incr
            m += 1
        
        self.abc2n_dict = alpha
        return self.setup('letters')
        
    def setupNumDict(self, zero=int(), one=int(), two=int()):
        
        request = f"give a number value for "
        
        if not zero: zero = UserInput(request=request+'0',
                        default=str(0), response_type=int).getResponse()
        if not one: one = UserInput(request=request+'1', 
                        default=str(1), response_type=int).getResponse()
        if not two: two = UserInput(request=request+'2', 
                        default=one*2, response_type=int).getResponse()
        
        # new empty a2n dict
        nums = dict()
        # set number for a and increments to next numbers
        one, incr = one, two-one
        # set counter, mulltiplier
        m = 0
        nums['0'] = zero
        # create new a2n dict
        for char in range(1, 10):
            nums[str(char)] = one+m*incr
            m += 1
        self.num2n_dict = nums
        return self.setup('numbers')

    def letter2num(self, char):
        """ convert letter to a number """
        a2n_dict = {**self.abc2n_dict, **self.num2n_dict}
        # ignore digits by returning supplied character(s)
        if char not in a2n_dict:
            # add skipped char to skipped list
            self.skipped.append(char)
            print(f"skipping '{char}', not a2n_dict")
            return str()
        return a2n_dict[char]
    
    def convertString(self, string):
        """ convert letter to a number depending on user preference """
        s = string.replace('|', '')
        if s and not match(r"^\d+$", s):
            if match(r"^\D+$", s):
                if not self.setup_complete['letters']:
                    self.setup('letters')
            else:
                self.setup()
        # return converted string
        return ''.join([str(self.letter2num(c.lower())) for c in s])

    def getAlphaDict(self):
        """ return sorted a2n dictionary """
        return sorted(self.abc2n_dict, key=self.abc2n_dict.get)
    
    def getNumsDict(self):
        return sorted(self.num2n_dict, key=self.num2n_dict.get)
