import tkinter as tk


class ScrollFrameWidget(tk.Frame):
    def __init__(self, master, width: int, height: int, **kwargs):
        super().__init__(master, **kwargs)
        canvas = tk.Canvas(self, width=width, height=height)
        if 'bg' in kwargs:
            canvas.configure(bg=kwargs['bg'])
        canvas.configure(relief=tk.FLAT)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
