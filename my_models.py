from db import Db_manager

url = 'mongodb://localhost:37000/'
db = Db_manager(url)

class Prodotto(object):
    '''
        Classe adibita alla gestione dei prodotti mediante un oggetto
        che racchiude all'interno i propri parametri
    '''

    id = ''
    nome = ''
    produttore = ''
    prezzo = 0
    stok = 0
    categoria = ''

    def __init__(self, id, nome, produttore, prezzo, stok, categoria):
        '''
            Caricamento dei parametri

                - id : id del prodotto
                - nome : nome del prodotto
                - produttore : produttore del prodotto
                - prezzo : prezzo del prodotto singolo
                - stok : Quantita del prodotto in magazzino
                - categoria : categoria del prodotto
        '''

        self.id = id
        self.nome = nome
        self.produttore = produttore
        self.prezzo = prezzo
        self.stok = stok
        self.categoria = categoria
        pass

    def __str__(self):
        '''
            Permette di restituire una stringa formattata del produto
            con i sui parametri interni
        '''
        
        return f'Id : {self.id} Nome : {self.nome} Prezzo : {self.prezzo} Stok : {self.stok} Categories : {self.categoria}'

    def return_dict(self):
        '''
            Permette di restituire un dizionario del prodotto
            con i sui parametri interni
        '''
    
        return {'_id': self.id, 'nome': self.nome, 'prezzo': self.prezzo, 'stok': self.stok, 'categoria' : self.categoria}

    def ceck_prodotto(self, prodotto):
        '''
        
        '''

        if prodotto.id == self.id:
            return True
        return False


class Carrello(object):
    '''
        Questa classe gestisce il carello di un utente
    '''

    id_utente = ''
    lista = []

    def __init__(self, id_utente,lista=[]):
        self.id_utente = id_utente
        self.lista.append(lista)
        pass

    def carica_carello(self, lista):
        self.lista.append(lista)
        pass
    

class User(object):
    '''
        Questa classe gestisce l'utente
    '''

    id = ''
    username = ''
    __connection = False
    carrello  = Carrello(id_utente=id)

    def __init__(self,id, username, connection=False):
        '''
        
        '''
    
        self.id = id
        self.username = username
        self.__connection = connection
        pass

    def state_connected(self):
        '''
        
        '''

        return self.__connection

    def login(self):
        '''
        
        '''

        self.__connection = True
        pass

    def log_out(self):
        '''

        '''

        self.__connection = False
        pass

    def add_carrello(self, carrello):
        '''
        
        '''
    
        list_pod = []
        for prodotto in carrello:
            prod = Prodotto(id=prodotto['id'], 
                            nome=prodotto['nome'], 
                            prezzo=prodotto['prezzo'], 
                            stok=prodotto['stok'], 
                            categoria=prodotto['categoria'])
            list_pod.append(prod)

        self.carrello.carica_carello(list_pod)
        pass

    def add_prodotto(self, prodotto):
        '''
        
        '''

        prod = Prodotto(id=prodotto['id'], 
                            nome=prodotto['nome'], 
                            prezzo=prodotto['prezzo'], 
                            stok=prodotto['stok'], 
                            categoria=prodotto['categoria'])
        self.carrello.lista.append(prod)
        self.carica_carello()
        pass

    def carica_carello(self):
        '''
        
        '''

        db.riempi_carello(self.id, self.carrello)
        pass


class Controller(object):
    '''
        Questa classe gestisce il collegamneto degli utenti(utente)
    '''

    user = User(None, None)

    def set_utente(self, id, username):
        '''
        
        '''

        self.user = User(id, username)

    def login_utente(self, user):
        '''
        
        '''

        self.user.login()

    def log_out(self):
        '''
        
        '''

        self.user.log_out()

