from pyconsoleapp import ConsoleAppComponent

class StandardPageComponent(ConsoleAppComponent):

    def print(self, page_content):
        output = ''
        output = output+self.get_component('header_component').print()
        output = output+'{}'.format(page_content)
        output = output+'\n>>> '
        return output