from smartseed.ui.splash import Splash

class UserInput:
    """ class representing (forced) userinput """

    request = str()         # question or request to user
    response = str()        # (formatted) response from user
    default = str()         # default value when user inputs nothing
    rsp_type = str          # response type, str, bool, etc.

    # smartseed related
    showSplash = None   # function to display splash
    indent = (' '*(Splash.offset+2),
              ' '*(Splash.offset+4),
              ' '*4)
    # indent = ('', '', '')
    def __init__(self, request, default=None, response_type=rsp_type,
                no_indent=False, splash=None):
        """ initialise instance of class """
        if no_indent: self.indent = ('', '', '')
        self.request = request
        self.default = default
        self.rsp_type = response_type
        self.showSplash = splash

    def getResponse(self):
        """ return formatted response """
        return self.formatResponse(self.getUserInput())

    def getDefault(self):
        if self.default == None: return str()
        return self.rsp_type(self.default)
    
    def getUserInput(self):
        """ present user with request/question, return response """
        user_input = str()
        # loop over request, until an answer is given
        while not user_input:
            # show splash
            if self.showSplash: self.showSplash()
            # prompt user
            user_input = input(self.formatRequest()).strip()
            # return default response if none was given
            if not user_input and self.default: return self.getDefault()
        return user_input
    
    def formatResponse(self, user_input):
        """ return response in spcifiec type """
        return self.rsp_type(user_input)
    
    def formatRequest(self):
        """ return formatted request """
        return f"{self.indent[1]}{self.request}{self.formatDefault()}: "

    def formatDefault(self):
        """ return string of default response, if available """
        if self.default:
            return f"\n{self.indent[1]}- default setting is '{self.default}'"
        return str()

class ChoiceInput(UserInput):
    """ class representing froced user input with choices """

    choices = dict()
    
    def __init__(self, request, choices, default=str(), response_type=str,
                no_indent=False, splash=None):
        """ initialise instance of class """
        super().__init__(request, default, response_type, no_indent, splash)
        self.choices = choices

    def getOptions(self):
        """ return list of choice options """
        return list([str(c).lower() for c in self.choices])

    def inlineChoices(self):
        """ return string with choices """
        # choose char to separate options,
        # 2 options get 'or', the rest get '/'
        div = ' or ' if len(self.choices) == 2 else '/'
        return f"({div.join(self.getOptions())})"

    def formatRequest(self):
        """ return formatted request """
        request = f"{self.indent[0]}{self.request}{' '+self.inlineChoices()}"
        request += self.formatDefault()
        request += ': '
        return request
    
    def getUserInput(self):
        """ present user with request/question, return response """
        user_input = str()
        while user_input not in self.getOptions():
            # show splash
            if self.showSplash: self.showSplash()
            # prompt user
            user_input = input(f"{self.formatRequest()}").strip()
            # return default if no response given
            if not user_input and self.default != None: return self.getDefault()
        return user_input
    
class BoolChoice(ChoiceInput):
    """ class representing forced user input with boolean choice """

    def __init__(self, request, choices=None, default=None, response_type=bool,
                no_indent=False, splash=None):
        # inititate instance of class
        super().__init__(request, choices, default, response_type, no_indent, splash)
        self.request = request
        # set boolean choices
        self.choices = self.boolChoices()

    def formatResponse(self, choice):
        """ return response """
        for c in range(len(self.choices)):
            if choice in self.choices[c]: return self.rsp_type(c)

    def getOptions(self):
        """ return list of choice options """
        return sum(self.choices, list())

    def inlineChoices(self):
        """ return inline string with choices """
        # set True values
        y = self.choices[1][0]
        # capitalise default in choices list
        y = y.capitalize() if self.default in self.choices[1] else y
        
        # set False values
        n = self.choices[0][0]
        n = n.capitalize() if self.default in self.choices[0] else n
        
        return f"({'/'.join((y, n))})"

    def formatRequest(self):
        """ return formatted request with inline choices """
        request = f"{self.indent[0]}{self.request}{' '+self.inlineChoices()} "
        return request
                
    def boolChoices(self):
        """ return a tuple containing two lists containing choices """
        return (['no', 'nope', 'n', '0', False],
                ['yes', 'yep', 'y', '1', True])

class menuChoice(ChoiceInput):
    """ class representing forced user input with listable choices """

    heading = str()     # text above menu

    def __init__(self, request, choices, heading, default=None,
                response_type=int, no_indent=False, splash=None):
        """ initialise instance """
        super().__init__(request, choices, default, response_type, no_indent, splash)
        self.heading = heading    
        # print heading
        self.showDescription()
        # print menu
        self.showMenu()

    def showDescription(self):
        """ print formatted heading """
        print(f'{self.indent[0]}{self.heading}\n')
    
    def showMenu(self):
        """ print menu """
        for i in range(len(self.choices)):
            choice = self.choices[i]
            # print list number and choice option
            print(f'{self.indent[1]}{i + 1}. {choice}',
                   # mark default choice 
                   '(default)' if choice == self.default else '')
        print()
    
    def getDefault(self):
        """ return index of selection in choices list """
        return self.choices.index(self.default)+1

    def formatRequest(self):
        """ return formatted request """
        return f"{self.indent[0]}{self.request}: "

    def getOptions(self):
        """ return list of options """
        return list(str(i+1) for i in range(len(self.choices)))