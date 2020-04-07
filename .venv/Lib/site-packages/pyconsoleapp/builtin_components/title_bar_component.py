from pyconsoleapp.console_app_component import ConsoleAppComponent

class TitleBarComponent(ConsoleAppComponent):

    def print(self):
        output = self.app.name+'\n'
        return output