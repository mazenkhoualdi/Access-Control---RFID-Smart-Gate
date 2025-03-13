from flask import Flask, request, jsonify
from sqlalchemy import create_engine, text
from datetime import datetime

app = Flask(__name__)

# 📌 Connexion à SQL Server
server = "DESKTOP-J50K35E\\SQLEXPRESS"
database = "SAGEMCOM_DB"
connection_string = f"mssql+pyodbc://@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
engine = create_engine(connection_string)

@app.route('/evenement', methods=['POST'])
def handle_event():
    """
    Gérer un événement RFID (insertion ou mise à jour dans la table Evenement).
    """
    # Log des données reçues
    data = request.get_json()
    if not data:
        print("❌ Aucune donnée reçue")
        return jsonify({"message": "❌ Aucune donnée reçue"}), 400

    print(f"Données reçues : {data}")  # Log des données reçues

    # Vérification des données
    uid_badge = data.get("uid_badge")
    rfid_reader = data.get("rfid_reader")  # Identifie quel lecteur RFID a été utilisé (1 ou 2)

    if not uid_badge or not rfid_reader:
        print("❌ UID ou lecteur RFID manquant")
        return jsonify({"message": "❌ UID ou lecteur RFID manquant"}), 400

    try:
        with engine.connect() as conn:
            with conn.begin():  # Début de la transaction
                print("✅ Connexion à la base de données réussie")  # Log de connexion réussie

                # 🚀 Étape 1 : Vérifier si l'UID est B38838DA
                if uid_badge == "B38838DA":
                    id_alerte = 1  # Alerte : "Accès non autorisé - Badge invalide"
                    id_employe = conn.execute(text("SELECT id_employe FROM Employe WHERE nom_employe = 'Anonyme'")).scalar()
                    id_badge = conn.execute(text("SELECT id_badge FROM Badge WHERE uid_badge = :uid"), {"uid": uid_badge}).scalar()
                    if not id_badge:
                        # Si le badge n'existe pas, créer un nouveau badge
                        conn.execute(text("INSERT INTO Badge (uid_badge) VALUES (:uid)"), {"uid": uid_badge})
                        id_badge = conn.execute(text("SELECT id_badge FROM Badge WHERE uid_badge = :uid"), {"uid": uid_badge}).scalar()
                    print("⚠️ UID B38838DA détecté, alerte 1 déclenchée")
                else:
                    # 🚀 Étape 2 : Vérifier si l'UID existe dans la table Badge
                    badge_query = text("SELECT id_badge, id_employe FROM Badge WHERE uid_badge = :uid")
                    badge_result = conn.execute(badge_query, {"uid": uid_badge}).fetchone()

                    if badge_result:
                        id_badge, id_employe = badge_result
                        print(f"✅ Badge trouvé : ID {id_badge}, Employé {id_employe}")

                        # 🚀 Étape 3 : Vérifier si l'employé existe
                        if id_employe:
                            id_alerte = 6  # Alerte : "Accès accordé - Bienvenue !"
                            print(f"✅ Employé trouvé : ID {id_employe}")
                        else:
                            id_alerte = 5  # Alerte : "Badge non attribué à un employé valide"
                            print("⚠️ Badge non attribué à un employé valide")
                    else:
                        # 🚨 Si l'UID est inconnu, créer un nouveau badge et utiliser l'employé anonyme
                        conn.execute(text("INSERT INTO Badge (uid_badge) VALUES (:uid)"), {"uid": uid_badge})
                        id_badge = conn.execute(text("SELECT id_badge FROM Badge WHERE uid_badge = :uid"), {"uid": uid_badge}).scalar()
                        id_employe = conn.execute(text("SELECT id_employe FROM Employe WHERE nom_employe = 'Anonyme'")).scalar()
                        id_alerte = 5  # Alerte : "Badge non attribué à un employé valide"
                        print("⚠️ UID inconnu, création d'un nouveau badge et utilisation des valeurs anonymes")

                # 🚀 Étape 4 : Récupérer les valeurs anonymes pour les autres colonnes
                id_equipe = conn.execute(text("SELECT id_equipe FROM Equipe WHERE nom_equipe = 'Équipe Anonyme'")).scalar()
                id_poste = conn.execute(text("SELECT id_poste FROM Poste_Competence WHERE nom_poste = 'Poste Anonyme'")).scalar()
                id_emplacement = conn.execute(text("SELECT id_emplacement FROM Emplacement WHERE nom_emplacement = 'Emplacement Inconnu'")).scalar()

                # 🚀 Étape 5 : Gérer l'insertion ou la mise à jour selon le lecteur RFID
                if rfid_reader == 1:
                    # RFID1 : Insertion sans date_entree
                    insert_query = text("""
                        INSERT INTO Evenement (id_employe, id_badge, id_equipe, id_poste, id_alerte, id_emplacement)
                        VALUES (:id_employe, 
                                :id_badge, 
                                :id_equipe, 
                                :id_poste, 
                                :id_alerte, 
                                :id_emplacement)
                    """)
                    conn.execute(insert_query, {
                        "id_employe": id_employe,
                        "id_badge": id_badge,
                        "id_equipe": id_equipe,
                        "id_poste": id_poste,
                        "id_alerte": id_alerte,
                        "id_emplacement": id_emplacement
                    })
                    print("✅ Insertion dans la table Evenement réussie (RFID1)")  # Log de l'insertion réussie
                elif rfid_reader == 2:
                    # RFID2 : Vérifier si le badge est autorisé avant de mettre à jour
                    if id_alerte == 6:  # Seulement si l'alerte est "Accès accordé - Bienvenue !"
                        update_query = text("""
                            UPDATE Evenement
                            SET date_entree = :date_entree
                            WHERE id_badge = :id_badge AND date_entree IS NULL
                        """)
                        conn.execute(update_query, {
                            "date_entree": datetime.now(),
                            "id_badge": id_badge
                        })
                        print("✅ Mise à jour de la date_entree réussie (RFID2)")  # Log de la mise à jour réussie
                    else:
                        print("❌ Badge non autorisé, mise à jour ignorée")

                # Vérifiez l'insertion ou la mise à jour
                verification_query = text("SELECT * FROM Evenement WHERE id_badge = :id_badge")
                verification_result = conn.execute(verification_query, {"id_badge": id_badge}).fetchone()
                print(f"Vérification de l'insertion/mise à jour : {verification_result}")  # Log de la vérification

                return jsonify({"message": "✅ Événement enregistré/mis à jour avec succès"}), 201

    except Exception as e:
        print(f"❌ Erreur SQL : {str(e)}")  # Log des erreurs SQL
        return jsonify({"message": f"❌ Erreur SQL : {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)