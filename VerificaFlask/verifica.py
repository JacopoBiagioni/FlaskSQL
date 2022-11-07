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
 
# Realizzare un sito web che permetta di visualizzare tutti i dipendenti che lavorano in un certo store. Il manager inserisce il nome dello store e clicca su un bottone che
# invia i dati al server. Quest'ultimo accede al database e restituisce i nomi e i cognomi dei dipendenti di quello store. Se il nome dello store non è presente, deve essere
# restituito un opportuno messaggio di errore. Tutta la parte grafica deve essere gestita con Bootstrap.

@app.route('/', methods=['GET'])
def ricerca():
    return render_template("ricerca.html")
 
@app.route('/risultato', methods=['GET'])
def risultato():
    NomeStore = request.args['NomeStore']
    query = f"SELECT first_name, last_name FROM sales.staffs as sf INNER JOIN sales.stores as st ON sf.store_id = st.store_id WHERE store_name LIKE '{NomeStore}'"
    dfStores = pd.read_sql(query,conn)
    dati = list(dfStores.values.tolist())
    if dati == [] :
        return render_template('erroreStore.html')
    else:
        return render_template('risultato.html', nomiColonne = dfStores.columns.values, dati = list(dfStores.values.tolist()))


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)