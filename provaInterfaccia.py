import customtkinter
import os
import sys
sys.path.insert(1, os.path.join(os.getcwd(),"funzioni"))
from funzioni import leggiMagazzino

class ScrollableLabelButtonFrame(customtkinter.CTkScrollableFrame):
    def pFunction(self,item):
        print(f"+1 {item}")
    
    def mFunction(self,item):
        print(f"-1 {item}")

    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)

        self.command = command
        self.radiobutton_variable = customtkinter.StringVar()
        self.label_list = []
        self.pbutton_list = []
        self.mbutton_list = []

    def add_label(self, item):
        label = customtkinter.CTkLabel(self, text=item, compound="left", padx=5, anchor="w")
        label.grid(row=len(self.label_list), column=0, pady=(0, 10), sticky="w")
        self.label_list.append(label)

    def add_pbutton(self, item):
        button = customtkinter.CTkButton(self, text="+", width=50, height=24)
        button.configure(command=lambda: self.pFunction(item))
        button.grid(row=len(self.pbutton_list), column=1, pady=(0, 10), padx=5)
        self.pbutton_list.append(button)

    def add_mbutton(self, item, command=None):
        button = customtkinter.CTkButton(self, text="-", width=50, height=24)
        button.configure(command=lambda: self.mFunction(item))
        button.grid(row=len(self.mbutton_list), column=2, pady=(0, 10), padx=5)
        self.mbutton_list.append(button)

    def remove_item(self, item):
        for label, button in zip(self.label_list, self.button_list):
            if item == label.cget("text"):
                label.destroy()
                button.destroy()
                self.label_list.remove(label)
                self.button_list.remove(button)
                return
            

class App(customtkinter.CTk):
    path = os.path.join(os.getcwd(),"MAGAZZINO.xlsx")
    productList, qtyList, priceList = leggiMagazzino(path)

    def __init__(self):
        super().__init__()

        self.title("CTkScrollableFrame example")
        self.grid_rowconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)

        # create scrollable label and button frame
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.frame = ScrollableLabelButtonFrame(master=self, width=300, corner_radius=0)
        self.frame.grid(row=0, column=1, padx=0, pady=0, sticky="nsew")


        for item in self.productList:  # add items with images
            self.frame.add_label(item)
            self.frame.add_pbutton(item)
            self.frame.add_mbutton(item)


if __name__ == "__main__":
    customtkinter.set_appearance_mode("dark")
    app = App()
    app.mainloop()


