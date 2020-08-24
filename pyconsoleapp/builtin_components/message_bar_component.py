from textwrap import fill

from pyconsoleapp import ConsoleAppComponent, configs, styles


class MessageBarComponent(ConsoleAppComponent):
    def __init__(self, app):
        super().__init__(app)
        self.configure_printer(self.print_view)

    def print_view(self):
        output = ''
        if self.app.error_message:
            output = output+'/!\\ Error:\n{}\n'.format(
                fill(self.app.error_message, configs.terminal_width_chars)
            )
            output = styles.fore(output, 'red')
            output = output+('-'*configs.terminal_width_chars)+'\n'
            self.app.error_message = None
        if self.app.info_message:
            output = output+'[i] Info:\n{}\n'.format(
                fill(self.app.info_message, configs.terminal_width_chars)
            )
            output = styles.fore(output, 'blue')
            output = output+('-'*configs.terminal_width_chars)+'\n'
            self.app.info_message = None
        return output
