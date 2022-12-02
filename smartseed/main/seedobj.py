import hashlib
from re import match

from smartseed.main.gentoolkit import GenToolkit
from smartseed.ui.seedviewer import SeedViewer

class SmartSeed(GenToolkit):

    blen_min = int()      # set according to phrase_len, min entropy needed
    blen_max = int()      # set according to phrase_len, max entropy length
    
    user_input = str()    # string submitted by user
    e_usable = str()      # usable alphanum (+ spacer) chars
    e_numbrrr = str()     # string of numbers only, ready to convert to bits
    b_entropy = str()     # entropy converted to bits - before validation
    valid_bin = str()     # final binary string
    last_bins = list()

    mirrors = dict()

    def __init__(self, settings, seed_data=dict()):
        self.settings = settings
        self.phrase_length = settings.phrase_length 
        self.blen_min = settings.blen_min
        self.blen_max = settings.blen_max

        for key, value in seed_data.items():
            setattr(self, key, value)
    
    def getValidBinary(self, b_entropy=None):
        """ Hash binary string using linux terminal command  to complete binary_entropy """
        b = self.b_entropy[:self.blen_min] if not b_entropy else b_entropy[:self.blen_min]

        def convert_output_char(c):
            """ Return binary string converted from a digit or letter between a and f"""
            if not match('[0-9]', c):
                # convert letter to number, a to 10, b to 11, etc.
                c = ord(c) - 87
            else:
                c = int(c)
            # convert integer to binary
            return format(c, 'b').zfill(4)
        
        def bitstring_to_bytes(s):
            return int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='big')
        bits = bitstring_to_bytes(b)
        output = hashlib.sha256(bits).hexdigest()
        # convert each character to binary
        d1, d2 = convert_output_char(output[0]), convert_output_char(output[1])
        # concatenate converted binary strings to binary entropy
        valid_binary = str(b + d1 + d2)[:self.blen_max]
        if b_entropy: return valid_binary
        self.valid_bin = valid_binary

    def getLastBins(self):
        """ Print different options to use for last word """
        if self.blen_min < 256:
            return None
        b = self.b_entropy
        # generate all binary options
        options = [format(i, 'b').zfill(3) for i in range(8)]
        # format string to correct length
        b = b[:self.blen_min - 3]
        lastbins = list()
        for o in options:
            # find word assosiated with option
            o_bin = self.getValidBinary(b_entropy=b+o)
            lastbins.append(o_bin[-11:])
        self.last_bins = lastbins
    
    def getMirrors(self):
        primary = self.groupString(self.b_entropy)
        mirrors_dict = {'x': SmartSeed(self.settings), 
                        'y': SmartSeed(self.settings),
                        'z': SmartSeed(self.settings)}
        for m, seed_obj in mirrors_dict.items():
            seed_obj.user_input = f"{self.user_input} ({m}-mirrored)"
            seed_obj.e_numbrrr = self.b_entropy
            for b in primary:
                mirrors_dict[m].b_entropy += self.mirrorBinary(b, axis=m)
            seed_obj.getValidBinary()
            seed_obj.getLastBins()
            
        return mirrors_dict    
    
    @staticmethod
    def mirrorBinary(binary_string, axis=None):

        def horizontalMirror(s):
            return s[::-1]
        
        def verticalMirror(s):
            v = str()
            for c in s:
                v += '1' if c == '0' else '0'
            return v

        def diagonalMirror(s):
            return horizontalMirror(verticalMirror(s))

        m = str()
        if not axis:
            while m not in ('horizontal', 'h', 'x', 'vertical', 'v', 'y', 'both', 'b', 'z'):
                m = input('Please select an axis: horizontal, vertical or both? ')
        else:
            m = axis
        
        if m[0] in ('h', 'x'):
            return horizontalMirror(binary_string)
        elif m[0] in ('v', 'y'):
            return verticalMirror(binary_string)
        elif m[0] in ('b', 'z'):
            return diagonalMirror(binary_string)

    def showFinalResult(self):
        viewer = SeedViewer(self)
        viewer.revealAll()