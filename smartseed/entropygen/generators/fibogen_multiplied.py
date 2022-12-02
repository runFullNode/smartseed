from smartseed.entropygen.generators.fibogen import FiboGen

class MultiFiboGen(FiboGen):

    title = 'fibonacci multiplied'
    descr = 'generate a sequence based on fibonacci, multiplied'
    explain = f"""
    This method requires the user to provide a string of digits. A sequence
    of numbers will be generated based on fibonacci using given string of
    digits. Multiplication is used, instead of addition.

    ex: a = 2        ---> 2|4|8|32|256|8192|...(2, 2x2=4, 2x4=8, 4x8=32, etc)
        a = 20090103 ---> 20090103|403612238550609|8108611444542305522727|...
    """
    a = None

    def __init__(self, settings):
        super().__init__(settings)

    def generate(self, a=None, sections=True):
        """ fibonacci sequence multiplied """
        if not a: a = self.a
        b = int(a)
        e = str()
        section_count = 0
        while len(e) - section_count < self.min_length:
            b, a = a, a*b
            e += str(b)
            if sections: 
                e += str('|')
                section_count += 1
        return e[:self.min_length + section_count - 1]