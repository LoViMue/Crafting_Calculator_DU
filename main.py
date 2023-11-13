import tkinter as tk
from tkinter import filedialog
import pandas as pd
import craftingcalculator as cc

# Global variables
Crafting_List = []
Ore_List = []
ore_menge = []
price_menge = []
ent = []
vs = None
clicked = None
selected = 0
error = None

# Initialize the main application window
myapp = tk.Tk()
myapp.title("Louis's_Crafting_Calculator")

# Function to search for items based on user input
def Lettersearch():
    global vs, clicked
    try:
        vs.destroy()
    except Exception:
        print("List was not created")

    Sele = []
    Sele = Vor_schleage(was0.get())

    if Sele == []:
        for was in data:
            Sele.append(was)

    clicked = tk.StringVar()
    clicked.set(Sele[0])
    vs = tk.OptionMenu(myapp, clicked, *Sele)
    vs.grid(row=5, column=2, sticky="w")

# Placeholder function for Ores
def Ores():
    return

# Function to load data from a file
def Load():
    global Oreprice
    try:
        for i in range(len(Oreprice)):
            Oreprice[i].destroy()
    except Exception:
        print("List was not created")

    Oreprice = []
    for i, was in enumerate(Price_data["Price"]):
        Oreprice.append(tk.Label(myapp, text=was).grid(row=1 + i, column=4, padx=3, sticky="w"))

# Function to save user input to a file
def Save():
    global Price_data, Ore_List, error
    for i, was in enumerate(Price_data["Name"]):
        try:
            Ore = int(Ore_List[i].get())
        except Exception:
            Ore = 0

        if Ore != 0:
            Price_data["Price"][i] = Ore

    try:
        error.destroy()
    except:
        error = []

    try:
        Price_data.to_excel("Price_Data.xls")
        remove_error()
    except Exception as err:
        error = tk.Label(myapp, text=err)
        error.grid(row=0, column=2, padx=3, sticky="e")

    Load()

# Function for autocomplete suggestions based on user input
def Vor_schleage(gesucht):
    global error
    print(gesucht)
    Vor_schleage_liste = []
    for was in data:
        word_fraction = ""
        for letter in was:
            word_fraction += letter
            if word_fraction == gesucht:
                Vor_schleage_liste.append(was)
                break
            if letter == " " or len(word_fraction) >= len(gesucht) or letter == "-":
                if letter != " " or letter == "-":
                    word_fraction = letter
                else:
                    word_fraction = ""

    if len(Vor_schleage_liste) > 0:
        remove_error()
        return Vor_schleage_liste
    else:
        error = tk.Label(myapp, text="Nothing Found/No Input", fg="orange")
        error.grid(row=0, column=2, padx=3, sticky="e")
        return []

# Function to remove error messages
def remove_error():
    global error
    try:
        error.destroy()
    except Exception:
        print("There was no error")

# Function to add an item to the crafting list
def ADD():
    global Crafting_List, error, selected
    selected = 0
    try:
        if float(was1.get()) > 0:
            gesucht = [clicked.get(), float(was1.get())]
            remove_error()
    except Exception as err:
        error = tk.Label(myapp, text="1. Select the thing 2. Amount in 3. +", fg="red")
        error.grid(row=0, column=2, padx=3, sticky="e")

    Crafting_List.append(gesucht)
    update_crafting_list()
    Calculate()

# Function to remove an item from the crafting list
def remove_crafting_list_item():
    global Crafting_List, selected
    selected = 0
    Crafting_List.pop(selected)
    update_crafting_list()
    Calculate()

# Function to clear the entire crafting list
def clear_crafting_list():
    global Crafting_List, ore_menge
    Crafting_List = []
    update_crafting_list()
    Calculate()

# Function to update the crafting list display
def update_crafting_list():
    global error, ent, selected
    try:
        for was in ent:
            for wass in was:
                wass.destroy()
        ent = []
    except Exception:
        ent = []

    for i, was in enumerate(Crafting_List):
        ent.append([tk.Label(myapp, text=was[1]), tk.Label(myapp, text=was[0])])
        ent[0 + i][0].grid(row=6 + i, column=1, sticky="w")
        ent[0 + i][1].grid(row=6 + i, column=2, sticky="w")

        if i + 1 == len(Crafting_List):
            ent.append([tk.Button(myapp, text="del", command=remove_crafting_list_item),
                        tk.Button(myapp, text="Calculate", command=Calculate)])
            ent.append([tk.Button(myapp, text="Clear", command=clear_crafting_list), tk.Label(myapp, text="Placeholder")])
            ent.append([tk.Button(myapp, text="Up", command=SelectUp), tk.Button(myapp, text="Do", command=SelectDown)])
            ent[1 + i][0].grid(row=7 + i, column=1, sticky="w")
            ent[1 + i][1].grid(row=7 + i, column=2, sticky="w")
            ent[2 + i][0].grid(row=7 + i, column=1, sticky="e")
            ent[3 + i][0].grid(row=8 + i, column=1, sticky="w")
            ent[3 + i][1].grid(row=9 + i, column=1, sticky="w")

    if len(ent) != 0:
        ent[selected][0].destroy()
        ent[selected][0] = tk.Label(myapp, text=Crafting_List[selected][1], fg="red")
        ent[selected][0].grid(row=6 + selected, column=1, sticky="w")

# Function to select the next item in the crafting list
def SelectUp():
    global selected
    if len(ent)-4 != selected:
        selected += 1
    else:
        selected = len(ent)-4
    update_crafting_list()

# Function to select the previous item in the crafting list
def SelectDown():
    global selected
    if selected != 0:
        selected -= 1
    update_crafting_list()

# Function to calculate the cost based on the crafting list
def Calculate():
    global ore_menge, price_menge
    try:
        remove_widgets(ore_menge)
        remove_widgets(price_menge)
    except Exception as err:
        ore_menge = []
        print(err)

    if Crafting_List != []:
        gesucht = cc.Cordinator(data, skill_data, Crafting_List)
    else:
        return

    print(gesucht)
    ore_menge = []
    price_menge = []
    j = 0
    cost = 0

    for i, was in enumerate(Price_data["Name"]):
        for wass in gesucht:
            if was == wass[0]:
                ore_menge.append(tk.Label(myapp, text=round(wass[1])))
                ore_menge[j].grid(row=1 + i, column=5, padx=3, sticky="w")
                price_menge.append(tk.Label(myapp, text=round(wass[1]*Price_data["Price"][i]), fg="red"))
                price_menge[j].grid(row=1 + i, column=7, padx=3, sticky="w")
                cost += wass[1]*Price_data["Price"][i]
                j += 1

    if cost > 10000:
        if cost > 10000000:
            cost = str(round(cost / 1000000)) + "M"
        else:
            cost = str(round(cost / 1000)) + "k"
    else:
        cost = str(round(cost))

    price_menge.append(tk.Label(myapp, text=cost, fg="red"))
    price_menge[j].grid(row=2 + i, column=7, padx=3, sticky="w")

# Function to select the data file
def data_select():
    global data_select, data
    myapp.filename = filedialog.askopenfilename(title="Select A File", filetypes=(("json files", "*.json"), ("all files", "*.*")))
    data_select.configure(text=myapp.filename)
    data = pd.read_json(myapp.filename)

# Function to select the skill data file
def data_select2():
    global data_select2, skill_data
    myapp.filename = filedialog.askopenfilename(title="Select A File", filetypes=(("excel files", "*.xls"), ("all files", "*.*")))
    data_select2.configure(text=myapp.filename)
    skill_data = pd.read_excel(myapp.filename)

# Function to select the price data file
def data_select3():
    global data_select3, Price_data
    myapp.filename = filedialog.askopenfilename(initialdir="", title="Select A File", filetypes=(("excel files", "*.xls"), ("all files", "*.*")))
    data_select3.configure(text=myapp.filename)
    Price_data = pd.read_excel(myapp.filename)

    for i, was in enumerate(Price_data["Name"]):
        tk.Label(myapp, text=was).grid(row=1 + i, column=6, padx=3, sticky="w")
        Ore_List.append(tk.Entry(myapp, width=4))
        Ore_List[i].grid(row=1 + i, column=3, padx=3, sticky="w")

# Set up the user interface elements
tk.Label(myapp, text="Searchbar").grid(row=0, column=1, sticky="w")
tk.Button(myapp, text="Search", command=Lettersearch).grid(row=1, column=2, sticky="w")
tk.Button(myapp, text=" + ", command=ADD).grid(row=5, column=1, sticky="w")
was1 = tk.Entry(myapp, width=7)
was1.grid(row=5, column=1, sticky="w", padx=40)
tk.Label(myapp, text="Select").grid(row=4, column=2, sticky="w")
tk.Label(myapp, text="Change").grid(row=0, column=3, padx=3, sticky="w")
tk.Label(myapp, text="Price").grid(row=0, column=4, padx=3, sticky="w")
tk.Label(myapp, text="Ammount").grid(row=0, column=5, padx=3, sticky="w")
tk.Label(myapp, text="Ore").grid(row=0, column=6, padx=3, sticky="w")
tk.Label(myapp, text="Price").grid(row=0, column=7, padx=3, sticky="w")
tk.Label(myapp, text="recipes.jason").grid(row=0, column=8, padx=3, sticky="w")
data_select = tk.Button(myapp, text="-", command=data_select, width=15)
data_select.grid(row=1, column=8, padx=3, sticky="w")
tk.Label(myapp, text="Skill_list.xls").grid(row=2, column=8, padx=3, sticky="w")
data_select2 = tk.Button(myapp, text="-", command=data_select2, width=15)
data_select2.grid(row=3, column=8, padx=3, sticky="w")
tk.Label(myapp, text="Price_Data.xls").grid(row=4, column=8, padx=3, sticky="w")
data_select3 = tk.Button(myapp, text="-", command=data_select3, width=15)
data_select3.grid(row=5, column=8, padx=3, sticky="w")
Ore_List = []

tk.Button(myapp, text="Save", command=Save).grid(row=22, column=3, padx=3, sticky="w")
tk.Button(myapp, text="Load", command=Load).grid(row=22, column=4, padx=3, sticky="w")
tk.Button(myapp, text="Load", command=Load).grid(row=22, column=4, padx=3, sticky="w")
tk.Label(myapp, text="Summe", fg="green").grid(row=22, column=6, padx=3, sticky="w")

# Start the main application loop
myapp.mainloop()
