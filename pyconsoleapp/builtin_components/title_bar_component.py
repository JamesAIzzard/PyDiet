from pyconsoleapp import styles, Component


class TitleBarComponent(Component):
    _template = '''{app_name} | {route}'''

    def __init__(self, **kwds):
        super().__init__(**kwds)

    def printer(self, **kwds) -> str:
        """Returns title bar component view as string."""
        return self._template.format(
            app_name=styles.weight(self.app.name, 'bright'),
            route=styles.fore(self.app.current_route.replace('.', '>'), 'blue')
        )
