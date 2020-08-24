
from pyconsoleapp import ConsoleAppComponent

_template_with_title = '''{header}
{page_title}
{page_title_underline}
{page_content}
>>> '''
_template_without_title = '''{header}
{page_content}
>>> '''

class StandardPageComponent(ConsoleAppComponent):
    def __init__(self, app):
        super().__init__(app)
        self.configure_printer(self.print_view)

    def print_view(self, page_content: str, page_title: str = None):
        # Populate the correct template and return;
        if page_title:
            return _template_with_title.format(
                header=self.app.fetch_component(
                    'header_component').print(),
                page_title=page_title,
                page_title_underline=len(page_title)*'-',
                page_content=page_content)
        elif not page_title:
            return _template_without_title.format(
                header=self.app.fetch_component(
                    'header_component').print(),
                page_content=page_content)
