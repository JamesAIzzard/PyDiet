from pyconsoleapp.console_app_page import ConsoleAppPage
from pyconsoleapp.components.header import header
from pydiet.ui.components.main_menu import main_menu

class Home(ConsoleAppPage):
    pass

home = Home()
home.add_component(header)
home.add_component(main_menu)