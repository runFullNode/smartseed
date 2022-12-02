from smartseed.entropygen.entropygen import EntropyGen

class NumberSequence(EntropyGen):

    title = "number sequence"
    descr = "generate entropy using a primary number added to/multiplied by a second number"
    explain = f"""
    This basic method requires a primary and secondary number as well as
    an operator (addition or multiplication). The string will start with
    the primary number, followed by the primary number multiplied by or 
    added to the secondary number.
    The result is then multiplied by or added to the secondary number to
    create a new sum. This new sum gets added to string, before the 
    secondary number impacts it again to create the next piece string.

        pri_num = 1, sec_num = 2
     
        addition --> 135791113151719...(1, 1+2=3, 3+2=5, 5+2=7, etc)
        multiply --> 124816324896128...(1, 1x2=2, 2x2=4, 4x2=8, etc)

    Longer digits are more interesting and also require less work for the
    non-robotic among us. Using two dates could look something like this:

        pri_num = 20090103, sec_num = 20121128

        addition ---> 20090103|40211231|60332359|80453487|100574615...
        multiply ---> 20090103|404235533996184|81336749216855697755...
    """
    # set variables
    pri_num = None
    sec_num = None
    operator = None

    def __init__(self, settings):
        super().__init__(settings)
        self.seed_data['user_input'], self.seed_data['e_numbrrr'], self.seed_data['b_entropy'] = self.run()

    def run(self):
        u = self.getUserInput()
        f = self.generate()
        b = self.processEntropy(f)[1]
        if self.checkDoubles(b):
            return u, f, b
        else:
            print(f'using {u} unfortunately leads to duplicates in seed phrase. please try again.')
            return self.run()

    def getUserInput(self):
        """ get input from user, if needed """
        p = str()
        s = str()
        o = str()
        while not p:
            p = input(f'\n{self.indent}provide a primary number: ')
        self.pri_num = self.convertAlpha2Num(p)
        if p != self.pri_num:
            print(f'{self.indent}"{p}" converted to "{self.pri_num}"\n')
        while not s:
            s = input(f'{self.indent}provide secondary number: ')
        self.sec_num = self.convertAlpha2Num(s)
        if s != self.sec_num:
            print(f'{self.indent}"{s}" converted to "{self.sec_num}"')
        while o not in ('a', '+', 'm', '*', 'x'):
            o = input(f'\n{self.indent}choose operation, (a)ddition or (m)ultiplication: ').lower()
        self.operator = '+' if o in ('a', '+') else '*'
        
        return f'{self.title}: {self.pri_num} {self.operator} {self.sec_num}'

    def generate(self, a=None, b=None, o=None):
        
        a = self.pri_num if not a else a
        b = self.sec_num if not b else b
        o = self.operator if not o else o

        e = str()
        while len(e) < self.min_length:
            e += str(a)             # add current result to entropy
            a = eval(f"{a}{o}{b}")  # update current result
        return e[:self.min_length]