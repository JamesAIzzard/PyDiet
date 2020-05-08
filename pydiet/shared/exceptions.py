class UnknownUnitError(Exception):
    def __init__(self, *args):
        if len(args) and args[0]:
            super().__init__(args[0])