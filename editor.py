import csv

def convert(csvin):
    try:
        with open(csvin + '.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            o = open(csvin + '.txt', "w")
            for i,row in enumerate(reader):
                for j,column in enumerate(row):
                    if(column != ""):
                        o.write(column + " " + str(j * 50) + " " + str(500 + (13 - i) * -50) + "\n")
                        return "Completed succesfully"
    except:
        return "Error Occured, Is there a CSV with that name in the directory?"
