from smartseed.entropygen.entropygen import EntropyGen
from smartseed.ui.get_input import UserInput

class FiboGen(EntropyGen):

    title = 'fibonacci sequence'
    descr = 'generate a sequence based on fibonacci'
    explain = f"""
    This method requires the user to provide a string of digits. A sequence
    of numbers will be generated based on fibonacci using given string of
    digits.
    
    ex: a = 1        ---> 1|2|3|5|8|13|21|...  (1, 1+1=2, 2+1=3, 3+2=5, ...)
        a = 20090103 ---> 20090103|40180206|60270309|100450515|160720824|...
    """
    a = None

    def __init__(self, settings):
        super().__init__(settings)
        self.seed_data['user_input'], self.seed_data['e_numbrrr'], self.seed_data['b_entropy'] = self.run()
    
    def run(self):
        u = self.getUserInput()
        f = self.generate()
        b = self.processEntropy(f)[1]
        if not self.checkDoubles(b):
            self.showCheckError(u)
            return self.run()
        return u, f, b

    def getUserInput(self):
        converted = None
        request = f"\n{self.indent}please provide a number"
        u_input = UserInput(request).getResponse()
        converted = self.convertAlpha2Num(u_input)
        self.a = int(converted)
        return f'{self.title}: {u_input}{(" -> " + converted) if converted != u_input else ""}'

    def generate(self, a=None, sections=True):
        """ fibonacci based """
        if not a: a = self.a
        a = int(a)
        b = int()
        e = str()
        section_count = 0
        while len(e) - section_count < self.min_length:
            b, a = a, a+b
            e += str(a)
            if sections: 
                e += str('|')
                section_count += 1
        return e[:self.min_length + section_count - 1]