class Screen:
    def __init__(self):
        self.text = None
        self.back_screen = None
    
    def go_to(self, next_screen):
        n = next_screen()
        n.back_screen = self
        n.run()

    def go_back(self):
        self.back_screen.run()

    def run(self):
        raise NotImplementedError