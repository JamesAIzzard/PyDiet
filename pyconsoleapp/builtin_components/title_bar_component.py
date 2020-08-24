from pyconsoleapp import styles, ConsoleAppComponent


class TitleBarComponent(ConsoleAppComponent):
    def __init__(self, app):
        super().__init__(app)
        self.configure_printer(self.print_view)

    def print_view(self):
        output = '{app_name} | {route}\n'.format(
            app_name=styles.weight(self.app.name, 'bright'),
            route=styles.fore(self.app.route.replace('.', '>'), 'blue')
        )
        return output
