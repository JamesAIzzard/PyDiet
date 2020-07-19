from abc import abstractmethod

from pyconsoleapp import ConsoleAppComponent


class YesNoDialogComponent(ConsoleAppComponent):

    def __init__(self, app):
        super().__init__(app)
        self.message: str
        self.set_print_function(self.print)
        self.set_response_function(['-yes', '-y'], self.on_yes)
        self.set_response_function(['-no', '-n'], self.on_no)

    def print(self):
        # Define the template;
        template = '''
        {message}
        -yes, -y    -> Yes
        -no, -n     -> No
        '''    

        # Fill the template and return;
        output = template.format(
            message=self.message
        )
        output = self.app.fetch_component(
            'standard_page_component').call_print(content=output)
        return output

    @abstractmethod
    def on_yes(self):
        pass

    @abstractmethod
    def on_no(self):
        pass
