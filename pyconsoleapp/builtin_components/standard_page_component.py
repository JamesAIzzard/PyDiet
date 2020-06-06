from pyconsoleapp import ConsoleAppComponent

class StandardPageComponent(ConsoleAppComponent):
    def __init__(self, app):
        super().__init__(app)

    def print(self, page_content:str):
        output = ''
        output = output+self.app.fetch_component('header_component').print()
        output = output+'{}'.format(page_content)
        output = output+'\n>>> '
        return output