# REFERENCE
import customtkinter
from tkinter import messagebox
import os
import sys
import numpy as np
import pandas as pd
sys.path.insert(1, os.path.join(os.getcwd(),"Drive"))
from datetime import date

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

################################# CLASSI ###########################################################
class App(customtkinter.CTk):  
    def __init__(self):
        super().__init__()
        self.mainPath = os.getcwd()
        self.today = date.today().strftime("%d/%m/%Y")
        ################################ GET DATA ##################################################
        self.mainPath = os.getcwd()
        self.magPath = os.path.join(os.getcwd(),"tmp\\MAGAZZINO.csv")
        self.incPath = os.path.join(os.getcwd(),"tmp\\INCASSI.csv")
        self.resPath = os.path.join(os.getcwd(),"STORICO")
        # Magazzino
        self.df = pd.read_csv(self.magPath)
        self.storageDict = {
            "products":self.df["PRODOTTO"],
            "prices":np.asarray(self.df["PREZZO UNITARIO"]),
            "quantities":np.asarray(self.df["QUANTITA"]),
            "sells":np.zeros(len(self.df["PRODOTTO"])),
            "orders":np.zeros(len(self.df["PRODOTTO"]))
        }
        self.productList = self.storageDict["products"]
        # Incassi
        self.incassi = pd.read_csv(self.incPath)
        # Filename storico
        inFileName = os.path.join(self.resPath,date.today().strftime("%Y%m%d")+".txt")
        self.fileName = inFileName
        boolCond=False
        counter=1
        while boolCond==False:
            if os.path.exists(inFileName):
                self.fileName=os.path.join(self.resPath,date.today().strftime("%Y%m%d")+"_"+str(counter)+".txt")
                counter+=1
                inFileName=self.fileName
            else:
                boolCond=True

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
            command=lambda:self.close_order_function()
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
        # button.configure(command=lambda: buttonFunction(option, index, self.storageDict,self.order_textbox,self.total_textbox))
        button.configure(command=lambda: self.buttonFunction(option,index))
        button.grid(row=rowNum, column=colNum, pady=(0, 10), padx=5)
    
    def buttonFunction(self,option,index):
    # Read lists from dict
        products = self.storageDict["products"]
        sells = self.storageDict["orders"]
        prices = self.storageDict["prices"]
        quantities = self.storageDict["quantities"]
        quantity = quantities[index]
        if quantity > 0:
            # Clean resume textbox
            self.order_textbox.delete("1.0","end")
            self.total_textbox.delete("1.0","end")
            # Update sellList
            if option == "+":
                sells[index] += 1
            elif option == "-":
                sells[index] += -1    
            # Generate text for the resume textBox
            orderText = ""
            total = 0
            for product, sell, price in zip(products,sells,prices):
                if sell>0:
                    orderText += str(sell) + " x " + product.upper() + 7*"\t" + str(price*sell) + " €\n"
                    total = total+sell*price
            self.order_textbox.insert("0.0",orderText)
            self.total_textbox.insert("0.0", "Totale: " + str(total) + " €")
        else:
            messagebox.showerror(title="Errore magazzino",message="Prodotto non disponibile")
        # Update dict
        self.storageDict["orders"]=sells

    def close_order_function(self):
        # Filter negative order values
        self.storageDict["orders"][self.storageDict["orders"]<0]=0      
        # Update "MAGAZZINO.csv"
        self.df["QUANTITA"] = self.storageDict["quantities"]-self.storageDict["orders"]
        self.storageDict["quantities"] = self.df["QUANTITA"]
        self.df.to_csv(self.magPath,index=False)
    
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
        # Update self.incassi.csv
        revenue = 0
        for sell,price in zip(self.storageDict["sells"],self.storageDict["prices"]):
            revenue += sell*price
        revenue = round(revenue,2)
        if self.today not in list(self.incassi["DATA"]):
            revenue = str(revenue)
            revenue = revenue.replace(".",",")
            revenue = "€ "+revenue
            newRow = pd.DataFrame({"DATA":self.today,"VENDITE":revenue},index=[0])
            self.incassi = pd.concat([self.incassi,newRow])
        else:
            index = self.incassi[self.incassi["DATA"]==self.today].index[0]
            # from € to number
            value = self.incassi.at[index,"VENDITE"]
            value = value.replace("€ ","")
            value = value.replace(",",".")
            value = float(value)
            value += revenue
            # from number to €
            value = str(value)
            value = value.replace(".",",")
            value = "€ "+value
            self.incassi.at[index,"VENDITE"] = value
        self.incassi.to_csv(self.incPath,index=False)
        # Create summary file
        with open(self.fileName,"w") as f:
            f.write("DATA:\t"+self.today+"\n\n")
            tot = 0
            for product, price, sell in zip(self.storageDict["products"],self.storageDict["prices"],self.storageDict["sells"]):
                strLen = 50
                if sell>0:
                    t1 = str(sell) + " x " + product.upper()
                    t3 = str(round(price*sell,2)) + " €\n"
                    t2 = (strLen-len(t1)-len(t3))*" "
                    f.write(t1+t2+t3)
                tot += sell*price
            f.write("\n"+strLen*"-"+"\n")   
            t1="Totale:"
            t3=str(round(tot,2))+" €\n"
            t2 = (strLen-len(t1)-len(t3))*" "
            f.write(t1+t2+t3)
        answer = messagebox.askokcancel("Chiudi Cassa","Sei sicuro di voler chiudere la cassa?")
        if answer:
            self.destroy()

if __name__=="__main__":
    mainPath = os.getcwd()

    os.chdir(mainPath+"\\Drive")
    # CREATE ENVIRONMENT
    # Download data from Gdrive and store it into temporary files MAGAZZINO.csv and INCASSI.csv
    from Drive.Gdrive_utilities import read
    if not os.path.exists(os.path.join(mainPath,"STORICO")):
        os.mkdir(os.path.join(mainPath,"STORICO"))
    if not os.path.exists(os.path.join(mainPath,"tmp")):
        os.mkdir(os.path.join(mainPath,"tmp"))

    read(magPath=os.path.join(mainPath,"tmp","MAGAZZINO.csv"),
            incPath=os.path.join(mainPath,"tmp","INCASSI.csv"))

    os.chdir(mainPath)
    # RUN GUI
    # Run the graphical user interface with temporary files stored into the folder
    app = App()
    app.mainloop()

    os.chdir(mainPath+"\\Drive")
    # CLOSE APPLICATION
    # Run the Updload function and store all the modified files into the shared worksheet located into the Gdrive folder 
    from Drive.Gdrive_utilities import write
    write(magPath=os.path.join(mainPath,"tmp","MAGAZZINO.csv"),
        incPath=os.path.join(mainPath,"tmp","INCASSI.csv"))
    from Drive.Gdrive_utilities import upload
    upload(filePath=os.path.join(mainPath,"STORICO"))

    # CLEAR TEMPORARY FOLDERS
    import shutil
    shutil.rmtree(os.path.join(mainPath,"STORICO"))
    shutil.rmtree(os.path.join(mainPath,"tmp"))
    