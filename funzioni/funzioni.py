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
  
def buttonFunction(option,index,storageDict,textBox,resumeBox):
    # Read lists from dict
        products = storageDict["products"]
        sells = storageDict["orders"]
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
        textBox.insert("0.0",orderText)
        resumeBox.insert("0.0", "Totale: " + str(total) + " €")
        # Update dict
        storageDict["orders"]=sells
        return storageDict

if __name__ == "__main__":
    filePath=os.path.join(os.getcwd(),"MAGAZZINO.xlsx")
    
    productList, qtyList, priceList = leggiMagazzino(filePath)
    
    sellList = []
    for elem in qtyList:
        sellList.append(random.randint(0, 2))
    sellList = np.asarray(sellList)
    
    aggiornaMagazzino(filePath, productList, qtyList, sellList)

