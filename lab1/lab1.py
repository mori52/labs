import csv
import re
phone = '933156729'
bill = 0
parsed = []
# Parsing 
with open('data.csv') as file:
    inf = csv.reader(file)
    for elem in inf:
        if elem[1] == phone or elem[2] == phone:
            parsed.append(elem)
# Tarification
for row in parsed:
    time = re.findall(':\d{2}:', row[0])
    time = time[0].replace(':', '')
    time = int(time)
    ishod = row[1]
    calldur = float(row[3])
    smsnum = int(row[4])
    if int(time) < 30:
        if ishod == phone:
            bill += calldur * 3
    elif int(time) >= 30:
        bill += calldur * 2 
    if smsnum > 50:
        bill += (smsnum - 50) * 2
print(round(bill, 2))