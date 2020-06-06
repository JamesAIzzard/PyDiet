import colorama
colorama.init()

def fore(text:str, color:str)->str:
    code = getattr(colorama.Fore, color.upper())
    return code + text + colorama.Style.RESET_ALL

def back(text:str, color:str)->str:
    code = getattr(colorama.Back, color.upper())
    return code + text + colorama.Style.RESET_ALL
    
def weight(text:str, weight:str)->str:
    code = getattr(colorama.Style, weight.upper())
    return code + text + colorama.Style.RESET_ALL