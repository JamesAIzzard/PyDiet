from pyconsoleapp.console_app_component import ConsoleAppComponent

class StandardPage(ConsoleAppComponent):

    def run(self):
        output = ''
        output = output+self.insert_component('Header')
        output = output+self.child_output()
        output = output+self.insert_component('DoubleHR')
        return output

standard_page = StandardPage()