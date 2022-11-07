# Realizzare un sito web che permetta di visualizzare le informazioni riguardanti i clienti.
# Un componente dello staff richiama la rotta /infoUser dove sono presenti due text per l'inserimento del nome e del cognome del cliente ed un bottone per inviare le 
# informazioni, Una volta inviate, il sito risponde con tutte le informazioni relative a quel cliente, una sotto l'altra. Se il cliente non esiste, deve essere visualizzato un 
# opportuno messaggio di errore. Utilizzare Bootstrap per l'interfaccia grafica di tutte le pagine.

from flask import Flask, render_template, request, redirect, url_for, Response
app = Flask(__name__)
import pymssql
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import io
import random
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
conn = pymssql.connect(server = '213.140.22.237\SQLEXPRESS', user = 'biagioni.jacopo', password = 'xxx123##', database = 'biagioni.jacopo')

@app.route('/infoUser', methods=['GET'])
def ricerca():
    return render_template("infoUser.html")
 
@app.route('/risultato', methods=['GET'])
def risultato():
    Nome = request.args['Nome']
    Cognome = request.args['Cognome']
    query = f"select * from sales.customers where first_name = '{Nome}' and last_name = '{Cognome}' "
    df = pd.read_sql(query, conn)
    dati = list(df.values.tolist())
    if dati == []:
        return render_template('erroreUtente.html')
    else:
        return render_template('risultato2.html', nomiColonne = df.columns.values, dati = list(df.values.tolist()))


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)