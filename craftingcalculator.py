import pandas as pd

def Recept_Skill_Anpassung(skill_data, data, gesucht):
    crafting_recept = []
    surplus = []
    for i, was in enumerate(data[gesucht[0]][9].items()):
        crafting_recept.append(list(was))
        crafting_recept[i][1] *= (gesucht[1] / data[gesucht[0]][4])

    for i, was in enumerate(data[gesucht[0]][7].items()):
        surplus.append(list(was))
        surplus[i][1] *= -1 * (gesucht[1] / data[gesucht[0]][4])

    crafting_recept += surplus
    crafting_recept = Zusammenfassen_Ore(crafting_recept)
    print("____________________\n", "--Recept+Angepassung\n", crafting_recept, "<-Input/Output->", gesucht, "\n--------------------")
    for i, was in enumerate(crafting_recept):
        for j, wass in enumerate(skill_data["Name"]):
            if wass == gesucht[0]:
                crafting_recept[i][1] *= skill_data["In"][j] / skill_data["Out"][j]
                #print("____________________\n", "----Skill-Anpassung-\n", was,"<-", skill_data["In"][j] / skill_data["Out"][j], "<-", gesucht, "\n--------------------")

                break

    return crafting_recept


def Cordinator(data, skill_data, crafting_list):
    #Bricht Sachen in ihre bestannteile zurück bis nur noch die menge an benötigtem erz aufgelisted bleibt.
    #Helikopter,Warpdrive,ect-> Rotor,Motor,ect-> Stahlblatter,schrauben,ect-> Stahl,ect-> Eisenerz,ect.
    Ore_list_complete = []
    for i, was in enumerate(crafting_list):
        if data[was[0]][1] != "Ore" and data[was[0]][9] != {}:
            #Ore<---Pure<---Product<---Intermediary Part<---Complex Part<---Structural Part
            #Ruft sich so lange selbst auf bis nur noch Grund Rezepte übrig sind

            Ore_list = Cordinator(data, skill_data, Recept_Skill_Anpassung(skill_data, data, was))
            for j in Ore_list:
                Ore_list_complete.append(j)
        else:
        #Wenn das Ding in der List kein Teil ist sondern Ore wird es direkt auf die List geschrieben
            Ore_list_complete.append(was)
    #Faesst doppelte eintraege auf der Liste zusammen
    Ore_list_complete = Zusammenfassen_Ore(Ore_list_complete)
    return Ore_list_complete


def Zusammenfassen_Ore(Ore_list):
    #Fasst dopplete eintraege zu einem zusammen  nach Ore Typen und Filtert nicht relevante daten
    #print(Ore_list,"\nComes in \n")
    summedup_Ore_list = []
    compact_Ore_list = []
    compact_Ore_list.append(Ore_list[0])
    #Schaut wie viele Arten Ore es gibt und legt die auf eine Liste ohne summierung
    for Ore in Ore_list:
        for i in range(len(compact_Ore_list)):
            if Ore[0] == compact_Ore_list[i][0]:
                break
            if len(compact_Ore_list) == i+1:
                compact_Ore_list.append(Ore)
    # Summiert Gleiche Ores zusammen.
    for Ore in compact_Ore_list:
        summedup_Ore_list.append(Compacter(Ore_list, Ore))

    #print(compact_Ore_list, "\nCompacted?\n")
    return compact_Ore_list


def Compacter(Ore_list, Ore):
    #Summiert Liste mit Ores
    a = False
    for Ore2 in Ore_list:
        if Ore[0] == Ore2[0]:
            if a:
                Ore[1] += Ore2[1]
            else:
                a = True
    return Ore


def Price_calculation(Price_data, Ore_data):
    Price = 0
    for was in Ore_data:
        for i, wass in enumerate(Price_data["Name"]):
            if was[0] == wass:
                Price += Price_data["Price"][i]*was[1]
    return Price


if __name__ == "__main__":
    data = pd.read_json("recipes.json")
    skill_data = pd.read_excel("123.xls")
    inputdata = pd.read_excel("1234.xls")
    Price_data = pd.read_excel("Price_Data.xls")

    # Input Daten auflistung
    crafting_list = []
    for i, was in enumerate(inputdata["Name"]):
        crafting_list.append([was, inputdata["Ammount"][i]])

    gesucht = Cordinator(data, skill_data, crafting_list)
    gesucht.sort()
    Price = Price_calculation(Price_data, gesucht)

    for i in range(len(gesucht)):
        gesucht[i][1] = round(gesucht[i][1], 2)
    Price = round(Price)
    print("Ores calculated\n", gesucht, "\nPrice =", Price)






