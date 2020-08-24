from abc import abstractmethod

from pyconsoleapp import ConsoleAppComponent


class YesNoDialogComponent(ConsoleAppComponent):

    def __init__(self, app):
        super().__init__(app)
        self.message: str
        self.configure_printer(self.print_view)
        self.configure_responder(self.on_yes, args=[
            self.configure_valueless_primary_arg(name='yes', markers=['-yes', '-y'])
        ])
        self.configure_responder(self.on_no, args=[
            self.configure_valueless_primary_arg(name='no', markers=['-no', '-n'])
        ])

    def print_view(self):
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
            'standard_page_component').print(content=output)
        return output

    @abstractmethod
    def on_yes(self):
        pass

    @abstractmethod
    def on_no(self):
        pass
