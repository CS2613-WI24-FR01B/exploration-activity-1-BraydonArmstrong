import csv

csvin = input("Give the filename\n")
o = open(csvin + ".txt", "w")

with open(csvin + '.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for i,row in enumerate(reader):
        for j,column in enumerate(row):
            if(column != ""):
                o.write(column + " " + str(j * 50) + " " + str(500 + (13 - i) * -50) + "\n")