import tkinter as tk
import webbrowser


class TKWindow:
    def __init__(self, title, label1, label2, errormsg, classname, outfunc, link=None):
        # ---WINDOW---
        self.window = tk.Tk()
        self.window.title(title)
        self.window.geometry("400x400")
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(5, weight=1)

        # ---VARIABLES---
        self.errormsg = errormsg
        self.classname = classname
        self.outfunc = outfunc
        self.link = link

        # ---LABEL---
        title = tk.Label(text=label1)
        title.grid(column=0, row=0)

        description = tk.Label(text=label2)
        description.grid(column=0, row=1)

        # ---ENTRY---
        self.user_entry = tk.Entry()
        self.user_entry.focus_set()
        self.user_entry.grid(column=0, row=2)
        self.user_entry.bind("<Return>", (lambda event: self.output()))

        # ---BUTTON---
        button_name = tk.Button(text="Let's go", command=self.output)
        button_name.grid(column=0, row=3)
        button_name.bind("<Return>", (lambda event: self.output()))

        # ---LINK---
        if self.link:
            lbl = tk.Label(text=r"Card numbers examples", fg="blue", cursor="hand2")
            lbl.grid(column=0, row=5, sticky="S")
            lbl.bind("<Button-1>", lambda event: webbrowser.open_new(self.link))

        self.window.mainloop()

    # ---FUNCTIONS---
    # chooses the output
    def output(self):
        try:
            user_input = str(self.user_entry.get()).strip()
            card = self.classname(user_input)
            self.output_field(getattr(card, self.outfunc)())
        except ValueError:
            self.output_field(self.errormsg)

    # creates the text field
    def output_field(self, state):
        output_field = tk.Text(master=self.window, height=10, width=30)
        output_field.grid(column=0, row=4)
        output_field.insert(tk.END, state)
        output_field.configure(state='disabled')
