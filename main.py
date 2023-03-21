#!/usr/bin/env python
# coding: utf-8

# In[3]:


from os.path import isfile
import matplotlib.pyplot as plt
import pandas as pd

from shop import Warehouse, SellProd, Profit

if __name__=="__main__":
        
        def available_commands():
            """
            It shows all the available commands for this program. We'll call it later when the user need help
            and when an invalid command is used.
            """
            
            print("Available commands:\n"
                  "- add -> add items to the stock\n"
                  "- list -> take a look to the warehouse inventory\n"
                  "- sell -> proceed with purchases\n"
                  "- profits -> check out the profits\n"
                  "- help -> see available commands\n"
                  "- close -> close the program\n")
        
        cmd = None

        while cmd != "close":

            cmd = input("Insert command: ")

            if cmd == "add":

                product = input("Insert product: ")
                quantity = input("Quantity: ")
                buy_price = input("Buy price: ")
                sell_price = input("Sell price: ")
                
                wh = Warehouse(product, quantity, buy_price, sell_price)
                wh.add_product()

            elif cmd == "list":
                Warehouse.show()

            elif cmd == "sell":

                products = []
                quantities = []
                
                ask = None

                while ask != "no":
                    products.append(input("Insert product: "))
                    quantities.append(input("Insert quantity: "))

                    ask = input("\nDo you want to insert another product? \n")

                sp = SellProd(products, quantities)
                sp.sell()

            elif cmd == "profits":

                p = Profit()
                p.show_prf()

            elif cmd == "help":
                available_commands()

            elif cmd=="close":
                print("\nGoodbye!")

            else:
                print("Invalid command\n")
                available_commands()

