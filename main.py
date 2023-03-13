# REFERENCE
# - https://www.youtube.com/watch?v=iM3kjbbKHQU



import customtkinter
import os
import sys
import numpy as np
sys.path.insert(1, os.path.join(os.getcwd(),"funzioni"))
from funzioni import leggiMagazzino, buttonFunction

################################# AVVIO INTERFACCIA ################################################
# 1- Lettura prodotti a magazzino, creazione delle liste prodotto, quantità e prezzo
# 2- Creazione array sell per tener conto della quantità di prodotti venduti
# 2- Creazione della parte destra interfaccia: prodotti e tasti + e -
# 3- Creazione della parte di riepilogo in interfaccia
# 4- Creazione del pulsante chiudi ordine
# 5- Creazione casella con totale di ricavi della serata

################################# WORKFLOW #########################################################
# PULSANTE +: - aggiunge +1 alla riga corrispondente nell'array sell
#             - aggiunge +1 alla riga contenuta nella casella di riepilogo
# PULSANTE -: - aggiunge -1 alla riga corrispondente nell'array sell
#             - aggiunge -1 alla riga contenuta nella casella di riepilogo
# PULSANTE CHIUDI ORDINE: - aggiorna i valori della quantità (arrayQty-arraySell)
#                         - cancella la lista presente nella casella di riepilogo



################################# CHIUSURA INTERFACCIA #############################################
# PULSANTE X INTERFACCIA: - incolla il nuovo valore delle quantità all'interno dell'excel magazzino
#                         - aggiorna il file "REGISTRO_VENDITE" con il venduto della serata


################################# TODO #############################################################
# - FILTRO SULLO ZERO DELLA SELLLIST
# - AGGIUNGERE RIGA RESOCONTO ORDINI NEL TEXTBOX



################################# CLASSI ###########################################################
class ScrollableLabelButtonFrame(customtkinter.CTkScrollableFrame):
    
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)

        self.radiobutton_variable = customtkinter.StringVar()
        self.label_list = []
        self.pbutton_list = []
        self.mbutton_list = []

    def add_label(self, item):
        label = customtkinter.CTkLabel(self, text=item.upper(), compound="left", padx=5, anchor="w")
        label.grid(row=len(self.label_list), column=0, pady=(0, 10), sticky="w")
        self.label_list.append(label)

    def add_pbutton(self, index, storageDict, resumeBox, totalPriceBox):
        button = customtkinter.CTkButton(self, text="+", width=50, height=24)
        button.configure(command=lambda: buttonFunction("p",index, storageDict, resumeBox, totalPriceBox))
        button.grid(row=len(self.pbutton_list), column=1, pady=(0, 10), padx=5)
        self.pbutton_list.append(button)

    def add_mbutton(self, index, storageDict, resumeBox, totalPriceBox):
        button = customtkinter.CTkButton(self, text="-", width=50, height=24)
        button.configure(command=lambda: buttonFunction("m",index, storageDict, resumeBox, totalPriceBox))
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
            
class resumeFrame(customtkinter.CTkFrame):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1,weight=1)
        self.radiobutton_variable = customtkinter.StringVar()

    def addButton(self):
        closeButton = customtkinter.CTkButton(self,text="Chiudi Ordine",width=400,height=50)
        closeButton.grid(row=0,column=1,sticky="nsew")
        return closeButton

    def addResumeBox(self):
        totalPriceBox = customtkinter.CTkTextbox(self,width=400,corner_radius=0)
        totalPriceBox.grid(row=0,column=0,sticky="nsew")
        return totalPriceBox

            
class App(customtkinter.CTk):
    # Get data
    path = os.path.join(os.getcwd(),"MAGAZZINO.xlsx")
    productList, qtyList, priceList = leggiMagazzino(path)
    sellList = np.zeros(len(qtyList))
    storageDict = {
        "products":productList,
        "prices":priceList,
        "quantities":qtyList,
        "sells":sellList
    }

    def __init__(self):
        super().__init__()
        current_dir = os.path.dirname(os.path.abspath(__file__))

        pad = 3
        self.title("Registratore di cassa")
        self.geometry("{0}x{1}+0+0".format(
            self.winfo_screenwidth()-pad, self.winfo_screenheight()-pad))
        self.grid_rowconfigure(2, weight=1)
        self.columnconfigure(1, weight=1)


        self.resumeFrame = resumeFrame(master=self, width=800, height=50, corner_radius=0)

        # create resume order textbox
        self.resumeBox = customtkinter.CTkTextbox(master=self, width=800, corner_radius=0)
        self.resumeBox.grid(row=0, column=1, sticky="nsew")

        # create total price textbox
        self.totalPriceBox = self.resumeFrame.addResumeBox()

        # create close order button
        self.closeOrderButton = self.resumeFrame.addButton()

        # create scrollable label and button frame
        self.scrollFrame = ScrollableLabelButtonFrame(master=self, width=500, height=750, corner_radius=0)
        self.scrollFrame.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        for item in self.productList:  # add items with images
            index = self.productList[self.productList==item].index[0]
            self.scrollFrame.add_label(item)
            self.scrollFrame.add_pbutton(index,self.storageDict,self.resumeBox,self.totalPriceBox)
            self.scrollFrame.add_mbutton(index,self.storageDict,self.resumeBox,self.totalPriceBox)

        

        # # create lower buttons
        # orderEndButton = customtkinter.CTkButton(self, text="Chiudi ordine", width=400, height=50)
        # orderEndButton.grid(row=1, column=1, pady=(0, 10), padx=5)

if __name__ == "__main__":
    customtkinter.set_appearance_mode("light")
    customtkinter.set_default_color_theme("blue")
    app = App()
    app.mainloop()


