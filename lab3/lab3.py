import csv
from docx2pdf import convert
from docxtpl import DocxTemplate
from num2words import num2words
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
mobile = round(bill, 2)

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
web_traffic = round(total, 2)

def propis(s):
    s = s.split(',')
    if len(s) == 2:
        if len(s[1]) == 1:
            s[1] = s[1] + '0'
        if s[0] == '0':
            s[0] = 'ноль руб.'
            s[1] = num2words(s[1], lang='ru') # копейки
            s.append('коп.')
        else:
            r = list(s[0])
            k = list(s[1])
            s[0] = num2words(s[0], lang='ru') # рубли
            s[1] = num2words(s[1], lang='ru')
            s.insert(1, 'руб.')
            s.append('коп.')
    elif len(s) == 1:
        r = list(s[0])
        if s[0] != '0':
            s[0] = num2words(s[0], lang='ru') # рубли
            s.insert(1, 'руб.')
            s.append('ноль коп.')
        else:
            s[0] = 'ноль руб. ноль коп.'
    out = ' '.join(s)
    return out.capitalize()

total = mobile + web_traffic
taxes = total * 0.2
in_words = propis(total)
doc = DocxTemplate('template.docx')
context = { 
'recipient.bank.name' : 'ПАО «Сбербанк»',
'recipient.bank.bik' : '041946000',
'recipient.bank.account ' : '30301810000006000001',
'recipient.inn' : '7707083893',
'recipient.kpp' : '773643001',
'recipient.account' : '70301830000073000004',
'recipient.name' : 'ООО «Зеленоглазое такси»', 
'bill.id' : '228',
'bill.date' : '17 мая 2020',
'recipient.address' : 'г. Санкт-Петербург, ул. Джона Рида, д.1', 
'customer.name': 'Цветкова М.А.', 
'customer.inn' : '3807583493',
'customer.kpp' : '923643041',
'customer.address': 'г. Череповец, ул. Первомайская, д. 64', 
'bill.reason' : '№300678 от 19.05.2019',
'mob.description': 'Мобильная связь и СМС',
'mob.price' : mobile,
'web.description': 'Интернет',
'web.price': web_traffic,
'bill.total' : total,
'bill.taxes': taxes,
'bill.total_in_words' : in_words,
'recipient.director' : 'Петров В. В.',
'recipient.accountant' : 'Гертд В. П.'
}
doc.render(context)
doc.save('list.docx')
convert('list.docx')
