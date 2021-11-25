import requests
import csv
from flask import Flask, render_template, redirect, request
app= Flask(__name__)

def read_csv():
    csvlist = {}
    with open('output.csv', newline='', encoding="UTF-8") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
        for row in spamreader:
            csvlist[row[1]] = row[3]
        return csvlist
        
def sciagnij():
    response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
    data = response.json()
    keys = data[0]["rates"][0].keys()
    with open("output.csv", "w", encoding='utf-8', newline="") as f:
        dict_writer = csv.DictWriter(f, keys, delimiter=';')
        dict_writer.writeheader()
        dict_writer.writerows(data[0]["rates"])
       
   
sciagnij()

@app.route('/', methods=['GET', 'POST'])
def kantor():
    if request.method == 'GET':
        return render_template('kantor.html')
    elif request.method == 'POST':
        waluta = request.form.get('waluta')
        amount = float(request.form.get('amount'))
        rates = read_csv()
        for rate in rates:
            if rate == waluta:
                score = float(rates[rate])
        print(score) 
        result = str(round(amount * score, 3)) 
        return render_template('kantor.html', wynik = result)

