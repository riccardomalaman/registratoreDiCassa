# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 16:08:32 2023

@author: Riccardo Malaman
"""

import os
import random

import numpy as np
import openpyxl
import pandas as pd


def leggiMagazzino(filePath):
    # Leggi file di magazzino
    df = pd.read_excel(filePath, "MAGAZZINO")
    # Estrai la lista dei prodotti, le quantità e il prezzo unitario
    productList = df["PRODOTTO"]
    qtyList = np.asarray(df["QUANTITÀ"])
    priceList = np.asarray(df["PREZZO UNITARIO"])
    
    return productList, qtyList, priceList

def aggiornaMagazzino(filePath,qtyList,sellList):
    # Input: - file excel contenente i dati del magazzino
    #        - array con le quantità dei vari prodotti
    #        - array con le quantità vendute dei vari prodotti
    # Output: "MAGAZZINO.xlsx" aggiornato con le quantità a magazzino ricalcolate
    
    # NOTE: questa funzione va fatta runnare solo in chiusura dell'interfaccia 
    # registratore
    
    # Array delle quantità aggiornate
    newList = qtyList-sellList
    # Apri magazzino
    wb = openpyxl.load_workbook(filePath)
    ws = wb["MAGAZZINO"]
    # Aggiorna la colonna (C:) delle quantità 
    index = 2 #la colonna quantità inizia dalla seconda riga
    for element in newList:
        ws["C"+str(index)] = element
        index+=1
    # Scrivi il nuovo file
    wb.save(filePath)

# def pFunction(index,storageDict,textBox):
#         # Read lists from dict
#         products = storageDict["products"]
#         sells = storageDict["sells"]
#         prices = storageDict["prices"]
#         # Clean resume textbox
#         textBox.delete("1.0","end")
#         # Update sellList
#         sells[index] += 1
#         # Generate text for the resume textBox
#         orderText = ""
#         for product, sell, price in zip(products,sells,prices):
#             if sell>0:
#                 orderText += str(sell) + " x " + product.upper() + 7*"\t" + str(price*sell) + "€\n"
#             elif sell<0:
#                 # Sells filter: sell must not be lower than 0
#                 sell==0
#         textBox.insert("0.0",orderText)
#         # Update dict
#         storageDict["sells"]=sells
#         return storageDict
    
def buttonFunction(option,index,storageDict,textBox,resumeBox):
    # Read lists from dict
        products = storageDict["products"]
        sells = storageDict["sells"]
        prices = storageDict["prices"]
        # Clean resume textbox
        textBox.delete("1.0","end")
        resumeBox.delete("1.0","end")
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
                orderText += str(sell) + " x " + product.upper() + 7*"\t" + str(price*sell) + "€\n"
                total = total+sell*price
            elif sell<0:
                # Sells filter: sell must not be lower than 0
                sell==0
        textBox.insert("0.0",orderText)
        resumeBox.insert("0.0", "Totale: " + str(total) + " €")
        # Update dict
        storageDict["sells"]=sells
        return storageDict

if __name__ == "__main__":
    filePath=os.path.join(os.getcwd(),"MAGAZZINO.xlsx")
    
    productList, qtyList, priceList = leggiMagazzino(filePath)
    
    sellList = []
    for elem in qtyList:
        sellList.append(random.randint(0, 2))
    sellList = np.asarray(sellList)
    
    aggiornaMagazzino(filePath, productList, qtyList, sellList)

