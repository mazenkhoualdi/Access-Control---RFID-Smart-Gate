from flask import Flask, request, jsonify
import pyodbc
from sqlalchemy import create_engine, text
from datetime import datetime

app = Flask(__name__)

# 📌 Connexion à SQL Server
server = "DESKTOP-J50K35E\\SQLEXPRESS"
database = "SAGEMCOM_DB"
connection_string = f"mssql+pyodbc://@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
engine = create_engine(connection_string)

# 📌 Vérifier la connexion à la base de données
try:
    with engine.connect() as conn:
        print(f"[{datetime.now()}] ✅ Connexion SQL Server réussie !")
except Exception as e:
    print(f"[{datetime.now()}] ❌ Erreur connexion SQL Server : {str(e)}")

@app.route('/rfid', methods=['POST'])
def rfid():
    """ Vérifie l'UID du badge et renvoie les infos de l'employé. """
    # Récupérer les données JSON de la requête
    data = request.get_json()
    uid_badge = data.get("uid_badge")

    # Afficher l'UID reçu
    print("\n----------------------")
    print(f"[{datetime.now()}] 🔄 Requête reçue :")
    print(f"🔹 UID reçu : {uid_badge}")

    # Vérifier si l'UID est manquant
    if not uid_badge:
        print(f"[{datetime.now()}] ❌ Erreur : UID manquant dans la requête")
        print("----------------------\n")
        return jsonify({"message": "❌ UID manquant"}), 400

    try:
        with engine.connect() as conn:
            # Préparer et exécuter la requête SQL
            query = text("""
                SELECT e.Nom_Employe, e.Prenom_Employe 
                FROM Employe e
                JOIN Badge b ON e.id_employe = b.id_employe
                WHERE b.uid_badge = :uid
            """)
            result = conn.execute(query, {"uid": uid_badge}).fetchone()

            # Traiter le résultat de la requête
            if result:
                nom, prenom = result
                print(f"[{datetime.now()}] ✅ UID {uid_badge} trouvé :")
                print(f"   - Nom : {nom}")
                print(f"   - Prénom : {prenom}")
                print("----------------------\n")
                return jsonify({"message": "✅ Accès accordé", "nom": nom, "prenom": prenom}), 200
            else:
                print(f"[{datetime.now()}] ❌ UID {uid_badge} non trouvé dans la base de données.")
                print("----------------------\n")
                return jsonify({"message": "❌ Accès refusé"}), 403

    except Exception as e:
        # Gérer les erreurs SQL
        print(f"[{datetime.now()}] ❌ Erreur SQL : {str(e)}")
        print("----------------------\n")
        return jsonify({"message": f"❌ Erreur SQL : {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)