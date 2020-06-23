import copy

f = open("exel.txt", "r")
contents = f.read()
instList = contents.split("\n")
print(len(instList))
del instList[0]
del instList[-1]
dayList = list()
day = list()
currentday = 0

for i in instList:
    inst = i.split("\t")
    if not inst[2] == currentday:
        currentday = inst[2]
        if day:
            dayList.append(copy.deepcopy(day))
        day.clear()
    day.append(inst)

exel = list()

for d in dayList:
    aircount = 0
    airtotal = 0
    windcount = 0
    windtotal = 0
    windmax = 0
    windmin = 9999
    for i in d:
        if not i[5] == "NaN":
            aircount += 1
            airtotal += float(i[5])

        if not i[9] == "NaN":
            windcount += 1
            windtotal += float(i[9])

        if i[12].replace(" ", ""):
            if float(i[12]) > windmax:
                windmax = float(i[12])
            elif float(i[12]) < windmin:
                windmin = float(i[12])

    if aircount > 0:
        avair = airtotal/aircount
    else:
        avair = 0
    if windcount > 0:
        avwind = windtotal/windcount
    else:
        avwind = 0

    exelrow = ""
    exelrow += str(i[2]) + "\t"
    exelrow += str(i[1]) + "\t"
    exelrow += str(i[0]) + "\t"
    exelrow += str(round(avair, 2)) + "\t"
    exelrow += str(round(avwind, 2)) + "\t"
    exelrow += str(windmin) + "\t"
    exelrow += str(windmax) + "\n"
    exel.append(exelrow)
    print(exelrow)

bigstring = ""
for e in exel:
    bigstring += e

f = open("out.txt", "w+")
f.write(bigstring)
