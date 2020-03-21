from pyconsoleapp.console_app_component import ConsoleAppComponent

class StandardPage(ConsoleAppComponent):

    def print(self, page_content):
        output = ''
        output = output+self.app.get_component('Header').print()
        output = output+'{}'.format(page_content)
        return output