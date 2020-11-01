from pyconsoleapp import Component, styles


class MessageBarComponent(Component):
    """Component to display the info and error messages stored on the component."""
    _main_template = '''{content}
{hr}\n'''
    _info_template = '[i] Info: {message}'
    _error_template = '/!\\ Error: {message}'

    def __init__(self, app):
        super().__init__(app)

    def printer(self, **kwds) -> str:
        if self.app.error_message is not None:
            if self.app.error_message.replace(' ', '') == '':
                self.app.error_message = "An error occurred."
            return self._main_template.format(
                content=styles.fore(self._error_template.format(message=self.app.error_message), 'red'),
                hr=self.single_hr
            )
        elif self.app.info_message is not None and not self.app.info_message.replace(' ', '') == '':
            return self._main_template.format(
                content=styles.fore(self._info_template.format(message=self.app.info_message), 'blue'),
                hr=self.single_hr
            )
        else:
            return ''
