from pyconsoleapp.console_app_component import ConsoleAppComponent

class NavTrailComponent(ConsoleAppComponent):

    def print(self):
        trail = self.app.route.replace('.', '>')
        return trail+'\n'        