from smartseed.entropygen.entropygen import EntropyGen
from random import randint

class AutoGen(EntropyGen):
    """ generate entropy automatically """

    title = "auto-generate"
    descr = f"generate entropy automatically"

    provide_mirrors = False

    def __init__(self, settings):
        super().__init__(settings)
        b = self.run()
        self.seed_data['user_input'] = self.title
        self.seed_data['e_numbrrr'], self.seed_data['b_entropy'] = self.processEntropy(b)
    
    def run(self):
        print('auto-generating entropy...\n')
        entropy = self.generate()
        if self.checkDoubles(string=entropy):
            return entropy
        else:
            return self.run()

    def generate(self):
        e = str()
        while len(e) < self.min_length:
            e += str(randint(0, 9))
        return e