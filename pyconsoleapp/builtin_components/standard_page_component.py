from pyconsoleapp import ConsoleAppComponent

_TEMPLATE_WITH_TITLE = '''{header}
{page_title}
{page_title_underline}
{page_content}
>>>'''

_TEMPLATE_WITHOUT_TITLE = '''{header}
{page_content}
>>>'''

class StandardPageComponent(ConsoleAppComponent):
    def __init__(self, app):
        super().__init__(app)
        self.set_print_function(self.print)

    def print(self, page_content:str, page_title:str=None):
        if page_title:
            return _TEMPLATE_WITH_TITLE.format(
                header=self.app.fetch_component('header_component').call_print(),
                page_title=page_title,
                page_title_underline=len(page_title)*'-',
                page_content=page_content)
        elif not page_title:
            return _TEMPLATE_WITHOUT_TITLE.format(
            header=self.app.fetch_component('header_component').call_print(),
            page_content=page_content)
