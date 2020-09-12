from typing import Any

import colorama
colorama.init()

def fore(text:Any, color:str)->str:
    code = getattr(colorama.Fore, color.upper())
    return code + str(text) + colorama.Style.RESET_ALL

def back(text:Any, color:str)->str:
    code = getattr(colorama.Back, color.upper())
    return code + str(text) + colorama.Style.RESET_ALL
    
def weight(text:Any, weight:str)->str:
    code = getattr(colorama.Style, weight.upper())
    return code + str(text) + colorama.Style.RESET_ALL