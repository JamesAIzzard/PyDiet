import gui



class View(gui.labelled_entry_widget.View):
    def __init__(self, **kwargs):
        super().__init__(label_text="Cost: £", entry_width=10, **kwargs)
