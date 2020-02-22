import os
import json
import tkinter as tk
from pathlib import Path
from pydiet.user_interface.views.main_menu import MainMenu
from pydiet.user_interface.views.ingredient_menu import IngredientMenu
from pydiet.user_interface.views.ingredient_editor import IngredientEditor
from pydiet.user_interface.views.ingredient_name_editor import IngredientNameEditor
from pydiet.user_interface.views.ingredient_cost_editor import IngredientCostEditor

_cwd = str(Path.cwd())
_DISPLAY_CACHE_PATH = _cwd+'/pydiet/user_interface/datafile_cache/'
_DISPLAY_DICT_FILENAME = "displayed_dict_cache.json"
_DISPLAY_DICT_FILEPATH = _DISPLAY_CACHE_PATH+_DISPLAY_DICT_FILENAME
_HEADER_TEXT = '''
PyDiet:
=======
(b)ack, (q)uit
-----------------------------------'''
LOGO = '''______     ______ _      _
| ___ \\    |  _  (_)    | |
| |_/ /   _| | | |_  ___| |_
|  __/ | | | | | | |/ _ \\ __|
| |  | |_| | |/ /| |  __/ |_
\\_|   \\__, |___/ |_|\\___|\\__|
       __/ |
      |___/
'''


class UI():
    def __init__(self):
        self._header = _HEADER_TEXT
        # Configure data window;
        self._tk_root = tk.Tk()
        self._tk_root.title('PyDiet')
        self._text_window = tk.Text(self._tk_root)
        self._text_window.insert(tk.END, LOGO)
        self._text_window.pack()
        # Console view history;
        self.view_name_stack = []
        # Configure console views;
        self.views = {}
        self.views['main_menu'] = MainMenu()
        self.views['ingredient_menu'] = IngredientMenu()
        self.views['ingredient_editor'] = IngredientEditor()
        self.views['ingredient_name_editor'] = IngredientNameEditor()
        self.views['ingredient_cost_editor'] = IngredientCostEditor()        

    def _trail(self) -> str:
        trail = ""
        for stage in self.view_name_stack:
            trail = trail+stage.replace("_", " ")+">"
        return trail+'\n-----------------------------'

    def run(self):
        screen_name = "main_menu"
        self.view_name_stack.append(screen_name)
        res = None
        while not res == 'q':
            if screen_name == "":
                screen_name = self.view_name_stack[-1]
            if not screen_name in self.views.keys():
                screen_name = self.view_name_stack[-1]
            else:
                if not screen_name in self.view_name_stack:
                    self.view_name_stack.append(screen_name)
                self.clear_console()
                print(_HEADER_TEXT)
                print(self._trail())
                res = self.views[screen_name].show()
                if res == "b":
                    if len(self.view_name_stack) > 1:
                        self.view_name_stack.pop()
                        screen_name = self.view_name_stack[-1]
                else:
                    screen_name = self.views[screen_name].response_action(res)

    def clear_console(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_dict(self, data:dict) -> None:
        self._text_window.configure(state='normal')
        self._text_window.delete('1.0', tk.END)
        data_string = json.dumps(data, indent=2)
        self._text_window.insert(tk.END, data_string)
        self._text_window.configure(state='disabled')
        self._tk_root.update()

    def display_text(self, data:str) -> None:
        self._text_window.configure(state='normal')
        self._text_window.delete('1.0', tk.END)
        self._text_window.insert(tk.END, data)
        self._text_window.configure(state='disabled')
        self._tk_root.update()

    def set_window_title(self, title:str)->None:
        self._tk_root.title(title)     