import pandas as pd

def Recept_Skill_Anpassung(skill_data, data, gesucht):
    # Adjusts recipe quantities based on skill data
    crafting_recept = []
    surplus = []

    # Modify input recipe quantities
    for i, was in enumerate(data[gesucht[0]][9].items()):
        crafting_recept.append(list(was))
        crafting_recept[i][1] *= (gesucht[1] / data[gesucht[0]][4])

    # Modify surplus recipe quantities
    for i, was in enumerate(data[gesucht[0]][7].items()):
        surplus.append(list(was))
        surplus[i][1] *= -1 * (gesucht[1] / data[gesucht[0]][4])

    crafting_recept += surplus
    crafting_recept = Zusammenfassen_Ore(crafting_recept)
    
    print("____________________\n", "--Recipe + Adjustment\n", crafting_recept, "<-Input/Output->", gesucht, "\n--------------------")
    
    # Apply skill adjustments
    for i, was in enumerate(crafting_recept):
        for j, wass in enumerate(skill_data["Name"]):
            if wass == gesucht[0]:
                crafting_recept[i][1] *= skill_data["In"][j] / skill_data["Out"][j]
                break

    return crafting_recept


def Cordinator(data, skill_data, crafting_list):
    # Breaks down items into their components until only the required ore quantity remains
    Ore_list_complete = []

    for i, was in enumerate(crafting_list):
        if data[was[0]][1] != "Ore" and data[was[0]][9] != {}:
            Ore_list = Cordinator(data, skill_data, Recept_Skill_Anpassung(skill_data, data, was))
            for j in Ore_list:
                Ore_list_complete.append(j)
        else:
            Ore_list_complete.append(was)

    Ore_list_complete = Zusammenfassen_Ore(Ore_list_complete)
    return Ore_list_complete


def Zusammenfassen_Ore(Ore_list):
    # Combines duplicate entries and filters irrelevant data
    summedup_Ore_list = []
    compact_Ore_list = []
    compact_Ore_list.append(Ore_list[0])

    # Create a list without duplicate ores
    for Ore in Ore_list:
        for i in range(len(compact_Ore_list)):
            if Ore[0] == compact_Ore_list[i][0]:
                break
            if len(compact_Ore_list) == i + 1:
                compact_Ore_list.append(Ore)

    # Sum up identical ores
    for Ore in compact_Ore_list:
        summedup_Ore_list.append(Compacter(Ore_list, Ore))

    return compact_Ore_list


def Compacter(Ore_list, Ore):
    # Sums up a list of ores
    a = False
    for Ore2 in Ore_list:
        if Ore[0] == Ore2[0]:
            if a:
                Ore[1] += Ore2[1]
            else:
                a = True
    return Ore


def Price_calculation(Price_data, Ore_data):
    # Calculates the total price based on ore quantities and prices
    Price = 0
    for was in Ore_data:
        for i, wass in enumerate(Price_data["Name"]):
            if was[0] == wass:
                Price += Price_data["Price"][i] * was[1]
    return Price


if __name__ == "__main__":
    # Read data from files
    data = pd.read_json("recipes.json")
    skill_data = pd.read_excel("123.xls")
    inputdata = pd.read_excel("1234.xls")
    Price_data = pd.read_excel("Price_Data.xls")

    # Input data listing
    crafting_list = []
    for i, was in enumerate(inputdata["Name"]):
        crafting_list.append([was, inputdata["Ammount"][i]])

    # Perform calculations
    gesucht = Cordinator(data, skill_data, crafting_list)
    gesucht.sort()
    Price = Price_calculation(Price_data, gesucht)

    # Round quantities and display results
    for i in range(len(gesucht)):
        gesucht[i][1] = round(gesucht[i][1], 2)
    Price = round(Price)
    print("Ores calculated\n", gesucht, "\nPrice =", Price)
