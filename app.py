from flask import Flask, render_template, request, redirect, url_for, Response
#pip install flask pandas contextily geopandas matplotlib
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

@app.route('/', methods=['GET'])
def home():
    return render_template("home.html") 

@app.route('/selezione', methods=['GET'])
def selezione():
  scelta = request.args['scelta']
  if scelta == 'esercizio1':
    return redirect(url_for('esercizio1'))
  elif scelta == 'esercizio2':
    return redirect(url_for('esercizio2'))
  elif scelta == 'esercizio3':
    return redirect(url_for('esercizio3'))
  elif scelta == 'esercizio4':
    return redirect(url_for('search'))

@app.route('/esercizio1', methods=['GET'])
def esercizio1(): 
  query = 'SELECT category_name, count(*) as numero_prodotti FROM production.products INNER JOIN production.categories ON production.products.category_id = production.categories.category_id GROUP BY categories.category_name ORDER BY numero_prodotti DESC'
  global df
  df = pd.read_sql(query,conn)
  return render_template("esercizio1.html", nomiColonne = df.columns.values, dati = list(df.values.tolist()))

@app.route('/graficoes1', methods=['GET'])
def graficoes1():
    fig, ax = plt.subplots(figsize = (10,6))
    fig.autofmt_xdate(rotation = 90)
    ax.bar(df.category_name, df.numero_prodotti, color = 'g')
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/esercizio2', methods=['GET'])
def esercizio2(): 
  query = 'SELECT store_name, count(*) as numero_ordini FROM sales.stores INNER JOIN sales.orders ON sales.stores.store_id = sales.orders.store_id GROUP BY stores.store_name ORDER BY numero_ordini DESC'
  global df2
  df2 = pd.read_sql(query,conn)
  return render_template("esercizio2.html", nomiColonne = df2.columns.values, dati = list(df2.values.tolist()))

@app.route('/graficoes2', methods=['GET'])
def graficoes2():
    fig, ax = plt.subplots(figsize = (10,6))
    fig.autofmt_xdate(rotation = 90)
    ax.bar(df2.store_name, df2.numero_ordini, color = 'r')
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/esercizio3', methods=['GET'])
def esercizio3(): 
  query = 'SELECT brand_name, count(*) as numero_prodotti FROM production.products INNER JOIN production.brands ON production.products.brand_id = production.brands.brand_id GROUP BY brands.brand_name ORDER BY numero_prodotti DESC'
  global df3
  df3 = pd.read_sql(query,conn)
  return render_template("esercizio3.html", nomiColonne = df3.columns.values, dati = list(df3.values.tolist()))

@app.route('/graficoes3', methods=['GET'])
def graficoes3():
    fig = plt.figure()
    ax = plt.axes()
    cols = ['c','b','hotpink','yellow','red','brown'] 
    ax.pie(df3.numero_prodotti, colors = cols, labels=df3.brand_name)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/search', methods=['GET'])     
def search():
    return render_template('search.html')


@app.route('/esercizio4', methods=['GET'])     
def esercizio4():

    # Invio query al Database e ricezione informazioni
    NomeProdotto = request.args['NomeProdotto']
    query = f"select * from production.products where product_name like '{NomeProdotto}%' "
    dfProdotti = pd.read_sql(query,conn)

    # visualizzare le informazioni
    return render_template('esercizio4.html', nomiColonne = dfProdotti.columns.values, dati = list(dfProdotti.values.tolist()))


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True) 