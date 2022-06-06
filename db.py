from pymongo import MongoClient


class Db_manager:
    connetion = MongoClient() # MongoClient
    my_db = '' # Collegamento di itanza del db
    my_col = '' # Collegamento di istanza della collezione


    # Inizializza la connesione al server
    def __init__(self, url):
        self.connetion = MongoClient(url)
        self.my_db = self.connetion['Ecommers']
        pass
    

    # Posizionamento sulla collezione coretta
    def set_collezione(self, n_col):
        self.my_col = self.my_db[n_col]
        pass


    def __carica_singolo(self, collezione, json):
        self.set_collezione(collezione)

        self.my_col.insert_one(json)
        pass


    # Funzione che richiede i parametri in input del nuovo prodotto 
    def inserimento_prodotto(self, nome_prodotto, nome_produttore, prezzo, categoria, disponibilita):
        collezione = 'Prodotti'
        prodotto = {
            'nome_prodotto' : '',
            'nome_produttore' : '',
            'prezzo' : 0,
            'disponibilita' : 0,
            'categoria' : ''
        }

        prodotto['nome_prodotto'] = nome_prodotto
        prodotto['nome_produttore'] = nome_produttore
        prodotto['prezzo'] = prezzo
        prodotto['disponibilita'] = disponibilita
        prodotto['categoria'] = categoria

        try:
            self.__carica_singolo(collezione, prodotto)
            print('caricato con successo')
        except:
            print('caricamento non avvenuto')
        pass


    def inserimento_utente(self, user, pass_):
        collezione = 'Utenti'

        utente = {
            'user' : '',
            'pass' : '',
        }

        utente['user'] = user
        utente['pass'] = pass_

        try:
            self.__carica_singolo(collezione, utente)
            print('caricato con successo')
        except:
            print('caricamento non avvenuto')
        pass
    
    
    def ricerca_utente(self, user, pass_):
        my_query = {'user' : user, 'pass' : pass_}
        
        try:
            utente = self.my_col.find_one(my_query)
            return (utente, True)
        except:
            return False

    def ricerca_utente_id(self, id_utente):
        my_query = {'id_utente' : id_utente}
        
        try:
            utente = self.my_col.find_one(my_query)
            return utente
        except:
            return False

    def catalogo(self):
        self.set_collezione('Prodotti')

        try:
            prodotti = self.my_col.find()
            return prodotti
        except:
            return None

    def riempi_carello(self, id_utente, articolo):
        carello = {
            'id_utente' : '',
            'articol0' : '',
            'totale' : 0
        }

        collezione = 'Utenti'
        self.set_collezione(collezione)

        try:
            self.ricerca_utente_id(id_utente)

        except:
            print('utente non riconosciuto')
            return
        

        collezione = 'Carrello'

        try:
            self.__carica_singolo(collezione, articolo)
            print('caricamento sul carello avvenuto')
        except:
            print('errore')
        pass      

    def get_carello(self, id_utente):
        self.set_collezione('Carrello')

        my_query = { 'id_utente' : id_utente}

        carello = self.my_col.find_one(my_query)
        return carello
