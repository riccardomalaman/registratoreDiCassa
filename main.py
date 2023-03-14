# REFERENCE
import customtkinter
import os
import sys
import numpy as np
import pandas as pd
sys.path.insert(1, os.path.join(os.getcwd(),"funzioni"))
from funzioni import buttonFunction

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
# - aggiungere stampa file di resoconto e totale chiusura cassa quando si preme "x"



################################# CLASSI ###########################################################
class App(customtkinter.CTk):  
    def __init__(self):
        super().__init__()
        ################################ GET DATA ##################################################
        path = os.path.join(os.getcwd(),"MAGAZZINO.csv")
        self.df = pd.read_csv(path)
        self.storageDict = {
            "products":self.df["PRODOTTO"],
            "prices":np.asarray(self.df["PREZZO UNITARIO"]),
            "quantities":np.asarray(self.df["QUANTITA"]),
            "sells":np.zeros(len(self.df["PRODOTTO"])),
            "orders":np.zeros(len(self.df["PRODOTTO"]))
        }
        self.productList = self.storageDict["products"]

        ################################ GUI #######################################################
        self.font = "consolas"

        # configure window
        self.title("Registratore di cassa")
        self.geometry("1100x580")

        # configure grid layout (3x3)
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1), weight=1)

        # create sidebar with scrollable menu
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, width=400)
        self.scrollable_frame.grid(row=0,column=0,rowspan=3, padx=(10, 10), pady=(10, 10), sticky="nsew")
        self.scrollable_frame.grid_rowconfigure(3)
        rowNum = 0
        for item in self.productList:
            index = self.productList[self.productList==item].index[0]
            # label
            self.add_label(item,rowNum)
            self.add_button("+",index,rowNum,1)
            self.add_button("-",index,rowNum,2)
            rowNum += 1

        # create resume textbox
        self.order_textbox = customtkinter.CTkTextbox(self, width=1000, height=800, font=(self.font,20))
        self.order_textbox.grid(row=0, column=1, rowspan=2, columnspan=2, padx=(10, 10), pady=(10, 10))

        # create close order button
        self.close_order_button = customtkinter.CTkButton(self,width=200,height=50,text="Chiudi ordine",font=(self.font,20))
        self.close_order_button.configure(
            command=lambda:self.close_order_function(path)
        )
        self.close_order_button.grid(row=2,column=2,padx=(10,10),pady=(10,10))

        # create order total textbox
        self.total_textbox  =customtkinter.CTkTextbox(self,height=50,font=(self.font,20))
        self.total_textbox.grid(row=2,column=1,padx=(10, 10), pady=(10, 10), sticky="nsew")
        self.total_textbox.insert("0.0","Totale: ")

        # close button
        self.protocol("WM_DELETE_WINDOW",self.on_closing)

    ################################ FUNZIONI ##################################################
    def add_label(self, item, rowNum):
        label = customtkinter.CTkLabel(self.scrollable_frame, 
                                        text=item.upper(), 
                                        compound="right", 
                                        font=(self.font,14),
                                        padx=5, 
                                        anchor="w")
        label.grid(row=rowNum, column=0, pady=(0, 5), sticky="w")

    def add_button(self, option, index, rowNum, colNum):
        button = customtkinter.CTkButton(self.scrollable_frame, 
                                            text=option,
                                            font=(self.font,14),
                                            width=50, height=24)
        button.configure(command=lambda: buttonFunction(option, index, self.storageDict,self.order_textbox,self.total_textbox))
        button.grid(row=rowNum, column=colNum, pady=(0, 10), padx=5)

    def close_order_function(self,path):
        # Filter negative order values
        self.storageDict["orders"][self.storageDict["orders"]<0]=0      
        # Update "MAGAZZINO.xlsx"
        self.df["QUANTITA"] = self.storageDict["quantities"]-self.storageDict["orders"]
        self.df.to_csv(path)
        print("MAGAZZINO updated")
        # Update sellList
        self.storageDict["sells"] += self.storageDict["orders"]
        # Clear orderList
        self.storageDict["orders"] = np.zeros(len(self.storageDict["sells"]))
        # Clear order_box
        self.order_textbox.delete("1.0","end")
        # Clear total_box
        self.total_textbox.delete("1.0","end")
        self.total_textbox.insert("0.0","Totale: ")
    def on_closing(self):
        print("chiuso")
        self.destroy()

if __name__=="__main__":
    app = App()
    app.mainloop()