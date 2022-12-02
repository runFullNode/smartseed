from os import system

class GenToolkit:

    @staticmethod
    def clearScreen():
        system('clear')
    
    @staticmethod
    def groupString(string):
        """ Return list of strings of 11 len for given string """
        s = string.replace('|', '')
        l = len(s)
        # generate a list of 'filled groups'
        group = [s[0+11*i:11+11*i] for i in range(l // 11)]
        # if string has more chars, append last few chars to grouplist
        if len(s) % 11:
            group += [s[(11 * (l // 11)):]]
        return group

    @staticmethod
    def formatReadable(s):
        """ Return a string of len 11 formatted to '000 0000 0000' """
        return f'{s[:3]} {s[3:7]} {s[7:]}'

    @staticmethod
    def checkDoubles(string):
        g = GenToolkit.groupString(string)
        grouped = g[:24]
        unique_g = set(grouped)
        if len(grouped) != len(unique_g):
            return False
        return True

    @staticmethod
    def printChunks(list_of_strings, phrase_len):
        chunks = [[] for _ in range(len(list_of_strings))]
        for _ in range(len(list_of_strings)):
            chunks[_] = GenToolkit.groupString(list_of_strings[_])
        c = 0 
        for o in range(len(chunks[0][:phrase_len])):
            print(f'{str(c+1).rjust(2)}.', end=' '*2)
            for i in range(len(list_of_strings)):
                print(f'{GenToolkit.formatReadable(chunks[i][o]):<13}', end='   ')
            c += 1
            print('')
        [print() for _ in range(phrase_len - len(chunks[0]) + 1)]