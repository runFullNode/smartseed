from os import system

class Splash:
    total_length = 68
    top_maxlen = 23
    offset = 6
       
    top_msg = 'welcome to'
    btm_msg = 'simplifying steps to self-custody'

    def __init__(self, top_msg=str(), btm_msg=str()) -> None:
          if top_msg: self.top_msg=top_msg
          if btm_msg: self.btm_msg=btm_msg

    def showSplash(self, top_msg=str(), btm_msg=str()):

        _top, _btm = self.setMessages(top_msg=top_msg, btm_msg=btm_msg)
        system('clear')
    #   .-------.{_top                 }.--.  .-------.                 .--. 
        splash = f"""
       _______ {_top                 } __    _______                   __ 
      |     __|.--------..---.-..----.|  |_ |     __|.-----..-----..--|  |
      |__     ||        ||  _  ||   _||   _||__     ||  -__||  -__||  _  |
      |_______||__|__|__||___._||__|  |____||_______||_____||_____||_____|
      {_btm                                                              }
      
      """
        print(splash)
    
    def setMessages(self, top_msg=str(), btm_msg=str()):
        if not top_msg: top_msg = self.top_msg
        if not btm_msg: btm_msg = self.btm_msg

        toffset, boffset = self.getOffsets()
        
        msg_len = len(self.top_msg)
        top = ' '*toffset + self.top_msg + ' '*(self.top_maxlen-msg_len-toffset)

        msg_len = len(self.btm_msg)
        btm = ' '*boffset + self.btm_msg
        return (top, btm)

    def getOffsets(self):
        return (int((self.top_maxlen - len(self.top_msg))/4),
                int((self.total_length - len(self.btm_msg))*3/4))

class ExitSplash(Splash):

    top_msg = str()
    btm_msg = str()

    msg = ('thank you for using smartseed','',
           'if you found this app useful,',
           'please consider donating some satoshis', '')
    addres = 'bc1qf7d7pj6fd2wfz6tmw9gvuk4uwdepsgu5k8mm25'
    qr_code = (
        '▄▄▄▄▄▄▄   ▄ ▄▄  ▄ ▄▄▄ ▄▄▄▄▄▄▄',
        '█ ▄▄▄ █ ▀ ▀ ▄▀▄██▀  ▀ █ ▄▄▄ █',
        '█ ███ █ ▀█▀ ▀█▄▀▀▀ █▀ █ ███ █',
        '█▄▄▄▄▄█ █▀▄▀█ ▄▀█▀▄ █ █▄▄▄▄▄█',
        '▄▄▄▄▄ ▄▄▄█▀█ ▄▄██▄▀▀█▄ ▄ ▄ ▄ ',
        '▄▄▀█▀ ▄▀  █ ▀▀▄▄█  ▀█▀▀▀▀▄  ▀',
        '▄▄██▀▄▄ █▄▄ █▄█▄▀▄ ▄▀█ ▀▀▀▄▄ ',
        '▄ ▄ ██▄█ █ ▄▄▀▄▄███▀▀▄▀▀▀▀▄▄▀',
        '▄▀▀██ ▄██▀▀█ ▄▀▄▄▄▄ █▀▀█▀▄▄▄▀',
        '█▀▀█▄ ▄▀ ▀  ▀▄▀▄▀  ▀▀ ▀ ▀█▄▀▀',
        '█ █▀█▄▄█ █▄ █▄ █▄▄▀▀█▄█▄▄▀▄█▀',
        '▄▄▄▄▄▄▄ █ ▄▄▄ █▄█  ██ ▄ █▀ ▀▀',
        '█ ▄▄▄ █ ▄▀██  ▀█▀▄  █▄▄▄█▄▄██',
        '█ ███ █ █▄█ ▀█▄▄▀▄  █▄▄▄▄█▄█▀',
        '█▄▄▄▄▄█ █▄  █▀▄█▀▄ █▀▄▄ ██▄▀ ',
        '')

    def __init__(self):
        pass
    
    def showSplash(self):
        super().showSplash()
        self.showMessage()
        self.showQR()
        self.showAdress()

    def showMessage(self):
        for line in self.msg:
            offset = ' '*int((self.total_length-len(line))/2+self.offset)
            print(f'{offset}{line}')
    
    def showQR(self):
        for line in self.qr_code:
            offset = ' '*int((self.total_length-len(line))/2+self.offset)
            print(f'{offset}{line}')
        
    def showAdress(self):
        offset = ' '*int((self.total_length-len(self.addres))/2+self.offset)
        print(f'{offset}{self.addres}\n')