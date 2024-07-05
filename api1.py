from flask import Flask, jsonify,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Text

app = Flask(__name__)

# Configurazione della connessione al database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://gabriele:Gabry678@localhost:3306/automotosprint'
print("connessione al database {app}")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
db = SQLAlchemy(app)

# Definizione delle tabelle
class clienti(db.Model): ## nome classi lettera grande
    clientiId = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(45), nullable=False)
    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}



class ordine(db.Model):
    codordine = db.Column(db.Integer, primary_key=True)
    cliente = db.Column(db.Integer, db.ForeignKey('clienti.clientiId'), nullable=False)

# Ottieni tutti gli utenti
@app.route('/api1/clienti',methods=['GET'])
def cliente():

   if request.method=='GET':

        utenti=clienti.query.all()
        return jsonify({"utenti":[{"clientiId":utente.clientiId,"nome":utente.nome} for utente in utenti]})
@app.route('/api1/ordini/<string:fiat>/', methods=['GET'])

#1)Elenco degli ordini effettuati da uno specifico cliente:
def ordini(fiat):
        if request.method=='GET':
        # Recupera il testo dal corpo della richiesta
           result = db.session.query(ordine.codordine).join(clienti).filter(clienti.nome == fiat).all()


        # Simulazione di dati dell'ordine
        response_serializable = [
    {
        'codordine':ordine.codordine
        # Altri campi del cliente se necessario
    }
    for ordine in result
]

        return jsonify(response_serializable)

# Endpoint per aggiungere un nuovo ordine
@app.route('/api1/clienti', methods=['POST'])
def aggiungi_cliente():
     if request.method == 'POST':
        if request.is_json:
            dati_nuovo_cliente = request.get_json()
            nome_cliente = dati_nuovo_cliente.get('nome')

            if nome_cliente is not None:
                nuovo_cliente = clienti(nome=nome_cliente)
                db.session.add(nuovo_cliente)
                db.session.commit()
                return jsonify({"messaggio": "Cliente aggiunto con successo"})
            else:
                return jsonify({"errore": "Il campo 'nome' non può essere nullo"}), 400
        else:
            return jsonify({"errore": "Richiesta non valida, assicurati che il Content-Type sia application/json"}), 415


# Endpoint per aggiornare un ordine esistente
@app.route('/api1/clienti/<int:clientiId>',methods=['PUT'])
def aggiornamento(clientiId):
    cliente_aggiornamento=clienti.query.get(clientiId)
    
    if cliente_aggiornamento:
        if request.is_json:
            dati_aggiornamento = request.get_json()
            nuovo_nome=dati_aggiornamento.get('nome')

            if nuovo_nome:
                cliente_aggiornamento.nome = nuovo_nome
                db.session.commit()
                return jsonify({"messaggio": f"Cliente con ID {clientiId} aggiornato con successo"})
            else:
                return jsonify({"errore": "Il campo 'nome' è obbligatorio"}), 400
        else:
            return jsonify({"errore": "Richiesta non valida, assicurati che il Content-Type sia application/json"}), 415
    else:
        return jsonify({"errore": f"Cliente con ID {clientiId} non trovato"}), 404

@app.route('/api1/clienti/<int:clentiId>',methods=['PATCH'])
def patch_utente(clientiId):
    utente_aggiornamento=clienti.query.get(clientiId)
    if utente_aggiornamento:
        if request.is_json:
            dati_aggiornamento=request.get_json()
            nuovo_nome=dati_aggiornamento.get('nome')
            if nuovo_nome:
                utente_aggiornamento.nome=nuovo_nome
                db.session.commit()
                return jsonify({"messaggio": f"Utente con ID {clientiId} aggiornato con successo"})
            else:
                return jsonify({"errore": "Il campo 'nome' è obbligatorio"}), 400
        else:
            return jsonify({"errore": "Richiesta non valida, assicurati che il Content-Type sia application/json"}), 415
    else:
        return jsonify({"errore": f"Utente con ID {clientiId} non trovato"}), 404
    
@app.route('/api1/clienti/<int:clientiId>',methods=['DELETE'])

def elimina_utente(clientiId):
    utente_eliminazione=clienti.query.get(clientiId)

    if utente_eliminazione:
        db.session.delete(utente_eliminazione)
        db.session.commit()
        return jsonify({"messaggio": f"Utente con ID {clientiId} eliminato con successo"})
    else:
        return jsonify({"errore": f"Utente con ID {clientiId} non trovato"}), 404
if __name__ == '__main__':
    app.run(debug=True)
