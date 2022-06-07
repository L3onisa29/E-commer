from operator import imod
from flask import Flask, redirect, render_template, request, session, url_for
#from flask_sqlalchemy import SQLAlchemy
from form import Registration_form, Login_form, Prodotto_form
from db import Db_manager
from my_models import *

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

knn = KNeighborsClassifier(n_neighbors=3)




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
    '''
    Funzione creta per gestire le richieste del catalogo

        se è post -> reindirizzare al ceck out
        se è get:
            -inserimento dei un prodotto del catalogo

    '''
    if request.method == 'POST':
        pass

    if request.args:
        if request.args
        prodotto = Prodotto(id=request.args.get('id'), nome=request.args.get('nome'), produttore=request.args.get('nome_produttore'), prezzo=request.args.get('prezzo'), stok=request.args.get('stok'), categoria=request.args.get('categoria'))
        controller.user.add_prodotto(prodotto)
        

    prodotti  = db.catalogo()
    return render_template('catalogo.html', title = 'Prodotti', user=controller.user.id, prodotti= prodotti, connesso = controller.user.state_connected())

# Aggiunta nuovo prodotto
@app.route('/new-prodotto', methods = ['GET','POST'])
def new_prodotto():
    '''
    Pagina per aggingere un prodotto

        Questa pagina gestisce l'inserimento di nuovi prodotti tramite
        un form

    '''
    form = Prodotto_form()
    if request.method == 'POST':
        nome = request.form['nome']
        produttore = request.form['produttore']
        prezzo = request.form['prezzo']
        categoria = request.form['categoria']
        scorta = request.form['scorta']
        try:
            db.inserimento_prodotto(nome, produttore, prezzo, categoria, scorta)
            return redirect(url_for('catalogo', connesso = controller.user.state_connected()))
        except:
            return redirect(url_for('new_prodotto', connesso = controller.user.state_connected()))
    else:    
        return render_template('new_prodotto.html', form = form, connesso = controller.user.state_connected())


# Carello 
@app.route('/carrello', methods = ['GET', 'POST'])
def carello():
    '''
    Pagina che mostra il carello

        Questa pagina permette di mostrare il carello recuperato dal database
        e effetuare il ceck out

    '''
    carello = db.get_carello(controller.user.id)
    return render_template('carrello.html', title = 'Carrello', carello= carello, connesso = controller.user.state_connected(), carello_ = carello)


# Login page
@app.route('/login', methods = ['GET', 'POST'])
def login():
    '''
    Pagina per gestire il login

        Qusta pagina permette agli utenti di accedere al tuo account

    '''
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
            return redirect(url_for('login', connesso = controller.user.state_connected()))
    else:
        return render_template('login.html', title = 'Login', form = form, connesso = controller.user.state_connected())


# Pagigina di registrazione
@app.route('/registrazione', methods = ['GET', 'POST'])
def registrazione():
    '''
    Pagina per gestire la registrazione

        Questa pagina di registrazione contiene un form che permette
        agli utenti di registrarsi andado a salvare sul db i dati

    '''
    db.set_collezione('Utenti')

    form = Registration_form()
    if request.method == 'POST':
        user = request.form['user']
        pass_ = request.form['pass_']

        if not db.ricerca_utente(user, pass_):
            try:
                db.inserimento_utente(user, pass_)
                return redirect(url_for('login', connesso = controller.user.state_connected()))
            except:
                return redirect(url_for('registrazione', connesso = controller.user.state_connected()))
        else:
            return redirect(url_for('registrazione', connesso = controller.user.state_connected()))
    else:
        return render_template('registrazione.html', title = 'Registrazione', form = form, connesso = controller.user.state_connected())
    
# Log out page
@app.route('/log_out', methods = ['GET'])
def log_out():
    '''
    Pagina per il log_out

        Questa pagina reindirizza il client alla home

    '''
    controller.log_out()
    return redirect(url_for('index', connesso = controller.user.state_connected()))


if __name__ == '__main__':
    app.run()
