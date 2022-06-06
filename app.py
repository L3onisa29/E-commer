from flask import Flask, redirect, render_template, request, session, url_for
#from flask_sqlalchemy import SQLAlchemy
from form import Registration_form, Login_form, Prodotto_form
from db import Db_manager
from my_models import *


app = Flask(__name__)
app.config['SECRET_KEY'] = 'b34004572a3bb22eb8af01cfb813edf1'

url = 'mongodb://localhost:37000/'
db = Db_manager(url)

controller = Controller()


# Home page
@app.route('/')
def index():
    return render_template('index.html', title = 'Home', connesso = controller.user.state_connected())

# Catalogo
@app.route('/catalogo', methods = ['GET', 'POST'])
def catalogo():
    if request.method == 'POST':
        pass

    if request.args:
        prodotto = Prodotto(id=request.args.get('id'), nome=request.args.get('nome'), prezzo=request.args.get('prezzo'), stok=request.args.get('stok'), categoria=request.args.get('categoria'))
        controller.user.add_prodotto(prodotto)
        

    prodotti  = db.catalogo()
    return render_template('catalogo.html', title = 'Prodotti', prodotti= prodotti, connesso = controller.user.state_connected())

# Aggiunta nuovo prodotto
@app.route('/new-prodotto', methods = ['GET','POST'])
def new_prodotto():

    form = Prodotto_form()
    if request.method == 'POST':
        nome = request.form['nome']
        produttore = request.form['produttore']
        prezzo = request.form['prezzo']
        categoria = request.form['categoria']
        scorta = request.form['scorta']
        try:
            db.inserimento_prodotto(nome, produttore, prezzo, categoria, scorta)
            return redirect(url_for('catalogo'))
        except:
            return redirect(url_for('new_prodotto'))
    else:    
        return render_template('new_prodotto.html', form = form, connesso = controller.user.state_connected())


# Carello 
@app.route('/carrello', methods = ['GET', 'POST'])
def carello():

    return render_template('carrello.html', title = 'Carrello', connesso = controller.user.state_connected(), carello_ = carello)


# Login page
@app.route('/login', methods = ['GET', 'POST'])
def login():
    db.set_collezione('Utenti')

    form = Login_form()
    if request.method == 'POST':
        user = request.form['user']
        pass_ = request.form['pass_']

        if db.ricerca_utente(user, pass_):
            user, bol = db.ricerca_utente(user, pass_)
            controller.set_utente(id= user['_id'], username = user['user'])
            controller.user.login()
            return redirect(url_for('index', connesso = controller.user.state_connected()))
        else:
            print('non ci sono')
            return redirect(url_for('login'))
    else:
        return render_template('login.html', title = 'Login', form = form, connesso = controller.user.state_connected())


# Pagigina di registrazione
@app.route('/registrazione', methods = ['GET', 'POST'])
def registrazione():

    db.set_collezione('Utenti')

    form = Registration_form()
    if request.method == 'POST':
        user = request.form['user']
        pass_ = request.form['pass_']

        if not db.ricerca_utente(user, pass_):
            try:
                db.inserimento_utente(user, pass_)
                return redirect(url_for('login'))
            except:
                return redirect(url_for('registrazione'))
        else:
            return redirect(url_for('registrazione'))
    else:
        return render_template('registrazione.html', title = 'Registrazione', form = form, connesso = controller.user.state_connected())
    
# Log out page
@app.route('/log_out', methods = ['GET'])
def log_out():

    controller.log_out()
    return redirect(url_for('index', connesso = controller.user.state_connected()))


if __name__ == '__main__':
    app.run()