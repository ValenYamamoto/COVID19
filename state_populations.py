import csv

state_pop = {}
state_den = {}
abbr = {}

with open("states//states.csv") as file:
    reader = csv.reader(file)
    for row in reader:
        if row[0] != "State":
            abbr[row[0]] = row[1]


with open("nst-est2019-alldata.csv") as file:
    reader = csv.reader(file)
    for row in reader:
        if row[0] != "SUMLEV":
            if row[4] in abbr:
                state_pop[abbr[row[4]]] = int(row[16])
            else:
                state_pop[row[4]] = int(row[16])

with open("states//Population-Density By State.csv") as file:
    reader = csv.reader(file)
    for row in reader:
        if row[2] in abbr:
            state_den[abbr[row[2]]] = float(row[3])
