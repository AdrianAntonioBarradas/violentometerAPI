from flask import Flask, request
from flask_mysqldb import MySQL

from config import config

import pickle
import stanza
import analisis.TxtToPd as txttopd
import pandas as pd

stanza.download("es")
nlp = stanza.Pipeline("es")

app = Flask(__name__)
mysql = MySQL(app)

""" RECIBIR EL TXT """


@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files["file"]
    if file and file.filename.endswith(".txt"):
        content = file.read().decode("utf-8")
        # Realiza las operaciones que desees con el contenido del archivo
        # ...
     


        df = txttopd.panditas_android(content,nlp)
        
 

        return str(df["mensaje"]) #"Archivo recibido y procesado con éxito." 
    else:
        return "Error: archivo no válido."


""" FORMULARIO DE AYUDA """


@app.route("/formulario", methods=["POST"])
def handle_form():
    names = request.form.get("names")
    surnames = request.form.get("surnames")
    eventZone = request.form.get("eventZone")
    email = request.form.get("email")
    phone = request.form.get("phone")
    idPlatform = request.form.get("idPlatform")
    age = request.form.get("age")

    print(names)

     # Validar campos numéricos
    if age:
        age = int(age)
    else:
        age = None
    
    if idPlatform:
        idPlatform = int(idPlatform)
    else:
        idPlatform = None

    # Guardar los datos en la base de datos
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO formularioayuda (names, surnames, eventZone, email, phone, idPlatform, age) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (names, surnames, eventZone, email, phone, idPlatform, age))
    mysql.connection.commit()
    cur.close()

    return "Formulario recibido y procesado con éxito."


if __name__ == "__main__":
    app.config.from_object(config["development"])
    app.run()




def create_pipeline():
    stanza.download("es")
    nlp = stanza.Pipeline("es")
    return nlp

# with open('es_pipeline.pkl', 'wb') as f:
#     pickle.dump(create_pipeline, f)


def iniciaAnalisis(file):
    

    nlp = create_pipeline()


    df = txttopd.panditas_android(file,nlp)
