#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
from os.path import isfile
import matplotlib.pyplot as plt

import pandas as pd
from os.path import isfile
import matplotlib.pyplot as plt

class Warehouse:

    """
    Class that add items to the stock
    """
    
    def __init__(self, product, quantity, buy_price, sell_price):
        
        self.product = product
        self.quantity = quantity
        self.buy_price = buy_price
        self.sell_price = sell_price
        
        """
        product: str --name of the product, lowercase
        quantity: int --quantity of the product
        buy_price: float --price at which you buy the product
        sell_price: float --price at which you sell the product
        """
    
    
    def _check_file(self):
        
        """
        Check if the file is in the directory and create it.
        """
        
        if isfile("inventory.csv") == False:
            col = ["Products", "Quantity", "Buy price", "Sell price"]
            df = pd.DataFrame(columns = col)
            df.to_csv("inventory.csv", index=False)
            
            
    def _check_product(self):
        
        """
        Check if the product is a valid input.
        """
        
        # must be lowercase
        self.product = self.product.lower()
    
        # must not be an empty space
        if self.product == "":
            return True
            
    
    def _check_prod_existence(self, inv):
        
        """
        Check if the product already exists in the inventory.
        Input 'inv' is a dataframe for the file inventory.
        """
        
        if self.product in list(inv.index):
            return True
        else:
            return False

    
    def _check_value_type(self):
        
        """
        Check if values are valid inputs. Quantity must be an int, buy and sell prices must be float.
        """
        
        try:
            self.quantity = int(self.quantity)
            self.buy_price = float(self.buy_price)
            self.sell_price = float(self.sell_price)

        except ValueError:
            return False

        
    def _save_file(self, inv):
        
        """
        With this function we save the changes of 'inv' to the file inventory.csv, and print a summury of the products
        added to the inventory/warehouse.
        Input 'inv' is a dataframe for the file inventory.
        """
    
        inv.to_csv("inventory.csv")
        print(f"\n{self.product} X {self.quantity} has been added.\n")
    
    
    def add_product(self):
        
        """
        With this function begin the adding process.
        This function is the only one, with function show, tha can be called outside.
        All the other functions support this main function of this class.
        """
     
        self._check_file()
        
        inv = pd.read_csv("inventory.csv", index_col = "Products")

        if self._check_product() != True:
            
            if self._check_value_type() != False:
            
                if  self._check_prod_existence(inv) == True:

                    old_quant = int(inv.loc[self.product, "Quantity"])
                    inv.loc[self.product, "Quantity"] = old_quant + self.quantity
                    print(f"\n{self.product} was already existing so, old buy and sell prices were kept.\n")
                    self._save_file(inv)

                else:

                    inv.loc[self.product] = [self.quantity, self.buy_price, self.sell_price]
                    self._save_file(inv)
                    
            else:
                print("\nQuantity, buy price and sell price must be numbers!!!\n")
                
        else:
            print("\nYou didn't insert a product.")
      
    
    def show():
        
        """
        With this function we can show what is present in the warehouse by printing a dataframe and plotting it
        in alphabetical order.
        """
        
        # if the file doesn't exist, it means that nobody added new products to the stock
        if isfile("inventory.csv") == False:
            print("The inventory file doesn't exist yet, please add items to the stock before using this function.")
        
        else:
            inv = pd.read_csv("inventory.csv", index_col = "Products")
            inv = inv.sort_index() ## show the stock in alphabetical order
            print(inv)
            
            # plot inventory bar chart
            prod = list(inv.index)
            quan = inv["Quantity"]
            plt.barh(prod, quan, color="blue")
            plt.gca().invert_yaxis()
            plt.title("Inventory")
            plt.ylabel("Products")
            plt.xlabel("Quantity")
            plt.bar_label(plt.barh(prod, quan))
            plt.show()


# In[7]:


class SellProd:
    
    """
    This class sell the products available in the warehouse.
    """
    
    def __init__(self, products, quantities):
        
        self.products = products
        self.quantities = quantities
        
        """
        products: list str --name of the products that you want to sell, lowercase
        quantities: list int --list of the products' quantities that you want to sell
        """
      
    def _check_file(self, file = "sold.csv"):
        
        """
        Check if the file is in the directory and creates it.
        """
        
        if isfile(file) == False:
            col = ["Products", "Quantity", "Buy price", "Sell price"]
            df = pd.DataFrame(columns = col)
            df.to_csv(file, index=False)
            
        
    def _check_product(self, product, inv):
    
        """
        Check if the product is in the stock.
        The single product is taken from an initial list of products that is taken in input.
        Inv is a dataframe representing the inventory.csv file.
        """        
        
        if product in list(inv.index):
            return True
        
        else:
            print(f"\n{product} is not in the inventory.\n")
            return False
    
    
    def _check_values(self, product, quantity):

        """
        Allert for non numeric input. Quantity is taken from the list in input and must be an int value.
        The single product is taken from the list of products in input.
        """
        
        try:
            quantity = int(quantity)

        except ValueError:
            print(f"{product}'s quantity must be a number!!!\n")
            return False
    
    
    def _check_quantity(self, product, quantity, old_q_inv):
    
        """
        Check if this quantity can be purchased or not. The quantity required mustn't exceed the quantity in the stock.
        The single product is taken from the list of products in input.
        Old_q_inv is the quantity in the stock and it is obtained in the function _sell_cycle.
        """
        
        if quantity > old_q_inv:
            print(f"\nMaximum available quantity for {product} is {old_q_inv}.\n")
            return True
    
    
    def _check_sold_products(self, product, quantity, sold, inv):
    
        """
        If the product is already in the list of the sold products add the new quantity.
        If not, a new line in the file has to be created.
        Sold and inv are dataframes of the sold.csv and inventory.csv files.
        """          
        
        if product in list(sold.index):
            old_quant = sold.loc[product, "Quantity"]
            sold.loc[product, "Quantity"] = old_quant + quantity

        # if we never sold that product before we add a new row   
        else:
            sold.loc[product] = [quantity, inv.loc[product, "Buy price"], inv.loc[product, "Sell price"]]
      
    
    def _update_inventory(self, product, quantity, old_q_inv, inv):
    
        """
        Decrease the quantity in the inventory, and if it goes to zero delete the product from the warehouse. 
        The single product and quantity are taken from the list of products and quantities in input.
        Old_q_inv is the quantity in the stock and it is obtained from the function _sell_cycle.
        Inv is a dataframe representing the inventory.csv file.
        """
        
        update = inv.loc[product, "Quantity"] = old_q_inv - quantity
        update

        # if a product goes to zero delete the row from the invenory
        if update == 0:
            inv.drop(product, inplace=True)
     
    
    def _record_purchase(self, sold_product, sold_quantity, sold_price, product, quantity, inv):
    
        """
        Register the purchase to be shown at the end of the cycle.
        Sold product, quantity and price are the same product, quantity and price passed through the _sell_cycle.
        Inv is a dataframe representing the inventory.csv file.
        """
        
        sold_product.append(product)
        sold_quantity.append(quantity)
        sold_price.append(inv.loc[product, "Sell price"])
        
        return sold_product, sold_quantity, sold_price
    
    def _save_file(self, inv, sold):
    
        """
        Save the changes to the file inventory.csv, which products' quantities have been modified and sold.csv
        file that received new sold products or increased the quantity of the products already sold in the past.
        Inv and sold are dataframes of the sold.csv and inventory.csv files.
        """
        
        inv.to_csv("inventory.csv")
        sold.to_csv("sold.csv")
     
    
    def _show_purchase(self, sold_product, sold_quantity, sold_price):
        
        """
        We collected the details of a single purchse in _record_purchase function and at the end of _sell_cycle
        we want to show a summury of the purchase with this function.
        Takes in input the return of the _record_purchase function.
        """
        
        print("PURCHASE RECORDED\n")
        total = 0
        for p, q, pr in zip(sold_product, sold_quantity, sold_price):
            print(f"-> {q} X {p}: €{pr}")
            total += pr

        total = round(total, 2)
        print(f"\nTOTAL: €{total}")
     
    def _sell_cycle(self):
        
        """
        With this function we create a cycle that check every single product from the list of products taken as input.
        We use some of the functions above to check if the single product is a valid input and ti is purchasable.
        The single quantity is checked for its validity and the purchase is recorded.
        The changes in the inventory.csv and sold.csv files are recorded.
        """
    
        # create 3 empty lists where we can record the sold items and quantities, and relative prices
        sold_product = []
        sold_quantity = []
        sold_price = []

        for product, quantity in zip(self.products, self.quantities):
                
                # at every run of the cycle we need an updated dataframe for the inventory.csv and sold.csv files
                inv = pd.read_csv("inventory.csv", index_col = "Products")
                sold = pd.read_csv("sold.csv", index_col = "Products")
                
                # we wanna have lowercase products
                product = product.lower()

                if self._check_product(product, inv) == False:
                    continue
                else:
                    old_q_inv = int(inv.loc[product, "Quantity"]) # get quantity in the stock

                if self._check_values(product, quantity) == False:
                    continue

                if self._check_quantity(product, quantity, old_q_inv) == True:
                    continue

                self._check_sold_products(product, quantity, sold, inv)

                self._record_purchase(sold_product, sold_quantity, sold_price, product, quantity, inv)

                self._update_inventory(product, quantity, old_q_inv, inv)

                self._save_file(inv, sold)
        
        return sold_product, sold_quantity, sold_price
    
            
    def sell(self):
        
        """
        This function is the only one callable outside this class and it is the final step for the selling procedure.
        It calls all the internal functions, the most important is _sell_cycle which calls al the other internal
        functions to check the validity of the inputs an to record the purchase.
        Finally it shows a summury of the purchase.
        """
        
        assert isfile("inventory.csv") == True, "You must add products to the stock first!!"

        self._check_file()

        sell = self._sell_cycle()

        self._show_purchase(sell[0], sell[1], sell[2])


# In[ ]:


class Profit:
    
    """
    This class shows the profits
    """

    def show_prf(self):
        
        """
        This functions call the other two functions of this class to show the profits and to plot them.
        """
        
        # Check if the file sold.csv exists
        if isfile("sold.csv") == False:
            print("The file of the sold products doesn't exist yet, please insert 'sell' command to start selling.")
        
        s = self.get_profits()
        
        self._plot_profits(s)
    
    def get_profits(self):
        
        """
        This function gets the profits by taking the sold.csv file and transforming it in a dataframe.
        The dataframe is then modified and new colums are added in order to calculate total costs and revenues,
        and finally to get the profit for each product sold. The sum of the last column 'profit' gives the total profit.
        """
        
        sold = pd.read_csv("sold.csv", index_col = "Products") 
        sold["Cost"] = sold["Quantity"]*sold["Buy price"]
        sold["Revenue"] = sold["Quantity"]*sold["Sell price"]
        tot_cost = sold["Cost"].sum()
        tot_revenue = sold["Revenue"].sum()
        profit = round(tot_revenue - tot_cost, 2)

        print(f"The activity generated revenues equal to {tot_revenue}.\n"
             f"The cost of the sold products is {tot_cost}.\n"
             f"Thus, the net profit is {profit}.")
        
        return sold
    
    
    def _plot_profits(self, sold):
        
        """
        With this function we take the dataframe 'sold' modified with the get_profits function and plot it.
        Then we print a list of the three products that generated more profits.
        """
    
        sold["Profit"] = sold["Revenue"] - sold["Cost"]
        sold = sold.sort_values("Profit", ascending = False)
        prod = list(sold.index)
        prof = sold["Profit"]
        m = prof[0:3]
        m = m.to_string(header = False)
        print(f"\nProducts that generated more profits:\n\n {m}")
        plt.barh(prod, prof, color="blue")
        plt.gca().invert_yaxis()
        plt.title("Profits by product")
        plt.ylabel("Products")
        plt.xlabel("Profits")
        plt.bar_label(plt.barh(prod, prof))
        plt.show()

