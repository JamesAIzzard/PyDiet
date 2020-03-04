from pyconsoleapp.console_app_component import ConsoleAppComponent

class StandardPage(ConsoleAppComponent):

    def run(self):
        output = ''
        output = output+self.insert_component('header')
        output = output+self.child_output()
        output = output+self.insert_component('double_hr')
        return output

standard_page = StandardPage()