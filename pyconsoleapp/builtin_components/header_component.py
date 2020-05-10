from pyconsoleapp.console_app_component import ConsoleAppComponent


class HeaderComponent(ConsoleAppComponent):

    def print(self):
        output = ''
        output = output+self.app.fetch_component('title_bar_component').print()
        output = output+self.app.fetch_component('double_hr_component').print()
        output = output+self.app.fetch_component('nav_options_component').print()
        output = output+self.app.fetch_component('nav_trail_component').print()
        output = output+self.app.fetch_component('single_hr_component').print()
        output = output+self.app.fetch_component('message_bar_component').print()
        return output
