from flask import Flask, render_template, request 
#pip install flask pandas contextily geopandas matplotlib
app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template("home.html") #serve per restituire una stringa

@app.route('/selezione', methods=['GET'])
def selezione():
  scelta = request.args['scelta']
  if scelta == 'esercizio1':
    return redirect(url_for('esercizio1'))
  elif scelta == 'esercizio2':
    return redirect(url_for('esercizio2'))
  else:
    return redirect(url_for('esercizio3'))

@app.route('/esercizio1', methods=['GET'])
def esercizio1():
    return render_template("esercizio1.html")

@app.route('/result', methods=['GET'])
def result():
# Collegamento al database
    import pandas as pd
    import pymssql
    conn = pymssql.connect(server = '213.140.22.237\SQLEXPRESS', user = 'biagioni.jacopo', password = 'xxx123##', database = 'biagioni.jacopo')
    # Invio query al database e ricezione informazioni
    nomeprodotto = request.args['nomeprodotto']
    query = f"select * from production.products where product_name like '{nomeprodotto}%'" #  f(format) prima di una stringa = 'format' + string = serve per inserire una variabile all interno di una stringa
    dfprodotti = pd.read_sql(query,conn)
    # Visualizzare le informazioni 
    return render_template('result.html', nomiColonne = dfprodotti.columns.values, dati = list( dfprodotti.values.tolist()))


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True) 