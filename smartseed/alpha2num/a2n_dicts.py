def a2n_abc():
    """ return standard alphabet where 'a' represents 1 """
    return {chr(i+97):i+1 for i in range(26)}

def a2n_123():
    """ return standard alphabet with numbers where 1 represents 27 """
    nums = {str(i): i for i in range(10)}
    return nums

def a2n_deutsch():
    """ return german dictionary """
    specials = 'äöüß'
    extras = {i:len(a2n_abc())+1+specials.index(i) for i in specials}
    return {**a2n_abc(), **extras}

def a2n_duitsch():
    """ return alternate german dictionary """
    a2n_dict = dict()
    specials = {'a':'ä','o':'ö','s':'ß','u':'ü'}
    i = 0
    for l in range(97, 97+26):
        i += 1
        a2n_dict[chr(l)] = i
        if chr(l) in specials:
            i += 1
            a2n_dict[specials[chr(l)]] = i
    return a2n_dict