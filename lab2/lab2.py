import csv
import matplotlib.pyplot as plot 
ip = "192.168.250.3" 
k = 3
total = 0 
graphlines = [] 
with open("nfcapd_20200.csv") as file:
    inf = csv.reader(file)
    for line in inf:
        if (len(line) == 48) and (line[3] == ip or line[4] == ip): 
            total += int(line[12])
            graphlines.append(line)
# Перевод из байтов в мегабайты и умножение на нужный коэффициент 
total = (total * k) / (1024 * 1024)
print("Стоимость израсходонного трафика:", round(total, 2), "рублей.")
# График
xdots = []
ydots = []
x, y = 0, 0
plot.ylabel("Объем трафика в байтах")
plot.xlabel("Время передачи в секундах")
for line in graphlines:
    x += float(line[2]) 
    y += (float(line[12]) + float(line[14]))
    xdots.append(x)
    ydots.append(y)
plot.plot(xdots, ydots, lw = 3, color = '#e35fe3')
plot.show()
