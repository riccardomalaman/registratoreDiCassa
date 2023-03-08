import customtkinter
from funzioni import incremento,decremento,leggiMagazzino



def itemButton(frame,text,command):
    button = customtkinter.CTkButton(master=frame, text=text, command=command)
    button.pack(pady=12, padx=10)

def plusButton(frame,itemName,productList,sellList):
    button = customtkinter.CTkButton(master=frame, text="+", command=incremento(itemName,productList,sellList))
    button.pack(pady=4, padx=4)

def minButton(frame,itemName,productList,sellList):
    button = customtkinter.CTkButton(master=frame, text="-", command=decremento(itemName,productList,sellList))
    button.pack(pady=4, padx=4)




if __name__=="__main__":
    import numpy as np


    filePath = "C:\\Users\\ricca\\Desktop\\REGISTRATORE_CASSA\\MAGAZZINO.xlsx"
    # Leggi magazzino
    productList, qtyList, priceList = leggiMagazzino(filePath)
    sellList = np.zeros(len(qtyList))
    

    index = 2
    product = productList.iat[index]

    # Crea interfaccia
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")


    root = customtkinter.CTk()
    root.geometry("600x400")

    frame = customtkinter.CTkFrame(master=root)
    frame.pack(pady=20, padx=60, fill="both", expand=True)

    label = customtkinter.CTkLabel(master=frame, text="REGISTRATORE DI CASSA")
    label.pack(pady=12,padx=10)

    entry1 = customtkinter.CTkEntry(master=frame, placeholder_text=product)
    entry1.pack(pady=12,padx=10)

    plusButton(frame,product,productList,sellList)
    minButton(frame,product,productList,sellList)


    




