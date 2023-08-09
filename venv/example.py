dict = { "Joe": 27, "Richie": 26, "Pierre":25, "Franklin":2, "Danny":14}

toCheck = "Richie Franklin Joe Joe Danny Pierre Franklin Pierre Pierre Pierre Joe Danny Richie Richie"
toCheck = toCheck.split()

dict = sorted(dict.items(), key=lambda x: x[1], reverse=True)

#After sort index correponds to word frequency
dictList = []

for key,_ in dict:
    dictList.append(key)

# ("Danny, 1) ("Richie", 4)
toCheck = sorted(toCheck, key=lambda x: dictList.index(x), reverse=True)

print(toCheck)
