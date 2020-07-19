from pyconsoleapp import ConsoleAppComponent


class StandardPageComponent(ConsoleAppComponent):
    def __init__(self, app):
        super().__init__(app)
        self.set_print_function(self.print)

    def print(self, page_content: str, page_title: str = None):
        # Define templates;
        with_title_template = '''{header}
        {page_title}
        {page_title_underline}
        {page_content}
        >>>'''
        without_title_template = '''{header}
        {page_content}
        >>>'''

        # Populate the correct template and return;
        if page_title:
            return with_title_template.format(
                header=self.app.fetch_component(
                    'header_component').call_print(),
                page_title=page_title,
                page_title_underline=len(page_title)*'-',
                page_content=page_content)
        elif not page_title:
            return without_title_template.format(
                header=self.app.fetch_component(
                    'header_component').call_print(),
                page_content=page_content)
