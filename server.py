from flask import Flask, request, jsonify
from sqlalchemy import create_engine, text
from datetime import datetime, timedelta

app = Flask(__name__)

# 📌 Connexion à SQL Server
server = "DESKTOP-J50K35E\\SQLEXPRESS"
database = "SAGEMCOM_DB"
connection_string = f"mssql+pyodbc://@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
engine = create_engine(connection_string)

# 🚀 ID de l'emplacement fixe pour RFID2
ID_EMPLACEMENT_RFID2 = 1  # Remplacez par l'ID de l'emplacement correspondant à RFID2

# 🚀 Heures de début des équipes (en fonction de l'ID de l'équipe)
HEURES_DEBUT_EQUIPE = {
    1: datetime.strptime("06:00:00", "%H:%M:%S").time(),  # Équipe 1 : 6h00
    2: datetime.strptime("14:00:00", "%H:%M:%S").time(),  # Équipe 2 : 14h00
    3: datetime.strptime("22:00:00", "%H:%M:%S").time(),  # Équipe 3 : 22h00
}

# Durée de travail d'une équipe (8 heures)
DUREE_EQUIPE = timedelta(hours=8)

def est_dans_intervalle_equipe(heure_actuelle, id_equipe):
    """
    Vérifie si l'heure actuelle est dans l'intervalle de l'équipe.
    """
    debut_equipe = HEURES_DEBUT_EQUIPE.get(id_equipe)
    if not debut_equipe:
        return False

    # Convertir l'heure de début en datetime
    debut_equipe_dt = datetime.combine(datetime.today(), debut_equipe)
    fin_equipe_dt = debut_equipe_dt + DUREE_EQUIPE

    # Convertir l'heure actuelle en datetime
    heure_actuelle_dt = datetime.combine(datetime.today(), heure_actuelle)

    # Si l'heure actuelle est avant l'heure de début, ajouter un jour (pour gérer les équipes de nuit)
    if heure_actuelle_dt < debut_equipe_dt:
        heure_actuelle_dt += timedelta(days=1)

    # Vérifier si l'heure actuelle est dans l'intervalle
    return debut_equipe_dt <= heure_actuelle_dt < fin_equipe_dt

def calculer_retard(heure_actuelle, id_equipe):
    """
    Calcule le retard par rapport à l'heure de début de l'équipe.
    """
    debut_equipe = HEURES_DEBUT_EQUIPE.get(id_equipe)
    if not debut_equipe:
        return None

    # Convertir l'heure de début en datetime
    debut_equipe_dt = datetime.combine(datetime.today(), debut_equipe)
    heure_actuelle_dt = datetime.combine(datetime.today(), heure_actuelle)

    # Si l'heure actuelle est avant l'heure de début, ajouter un jour (pour gérer les équipes de nuit)
    if heure_actuelle_dt < debut_equipe_dt:
        heure_actuelle_dt += timedelta(days=1)

    # Calculer le retard
    return heure_actuelle_dt - debut_equipe_dt

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

                # 🚀 Étape 1 : Vérifier si l'UID est non autorisé (exemple : B38838DA)
                if uid_badge == "B38838DA":
                    # Récupérer l'ID de l'alerte "Accès non autorisé - Badge invalide"
                    id_alerte = conn.execute(
                        text("SELECT id_alerte FROM Alerte WHERE message = :message"),
                        {"message": "Accès non autorisé - Badge invalide"}
                    ).scalar()
                    id_employe = conn.execute(text("SELECT id_employe FROM Employe WHERE nom_employe = :nom_employe"), {"nom_employe": "Anonyme"}).scalar()
                    id_badge = conn.execute(text("SELECT id_badge FROM Badge WHERE uid_badge = :uid"), {"uid": uid_badge}).scalar()
                    if not id_badge:
                        # Si le badge n'existe pas, créer un nouveau badge
                        conn.execute(text("INSERT INTO Badge (uid_badge) VALUES (:uid)"), {"uid": uid_badge})
                        id_badge = conn.execute(text("SELECT id_badge FROM Badge WHERE uid_badge = :uid"), {"uid": uid_badge}).scalar()
                    print("⚠️ UID B38838DA détecté, alerte 1 déclenchée")

                    # 🚨 Si RFID2 est utilisé pour un UID non autorisé, ne rien faire
                    if rfid_reader == 2:
                        print("❌ UID non autorisé détecté sur RFID2, aucune action effectuée")
                        return jsonify({"message": "❌ UID non autorisé, aucune action effectuée"}), 403
                else:
                    # 🚀 Étape 2 : Vérifier si l'UID existe dans la table Badge
                    badge_query = text("SELECT id_badge, id_employe FROM Badge WHERE uid_badge = :uid")
                    badge_result = conn.execute(badge_query, {"uid": uid_badge}).fetchone()

                    if badge_result:
                        id_badge, id_employe = badge_result
                        print(f"✅ Badge trouvé : ID {id_badge}, Employé {id_employe}")

                        # 🚀 Étape 3 : Vérifier si l'employé existe
                        if id_employe:
                            # Récupérer l'ID de l'alerte "Accès accordé - Bienvenue !"
                            id_alerte = conn.execute(
                                text("SELECT id_alerte FROM Alerte WHERE message = :message"),
                                {"message": "Accès accordé - Bienvenue !"}
                            ).scalar()
                            print(f"✅ Employé trouvé : ID {id_employe}")
                        else:
                            # Récupérer l'ID de l'alerte "Badge non attribué à un employé valide"
                            id_alerte = conn.execute(
                                text("SELECT id_alerte FROM Alerte WHERE message = :message"),
                                {"message": "Badge non attribué à un employé valide"}
                            ).scalar()
                            print("⚠️ Badge non attribué à un employé valide")
                    else:
                        # 🚨 Si l'UID est inconnu, créer un nouveau badge et utiliser l'employé anonyme
                        conn.execute(text("INSERT INTO Badge (uid_badge) VALUES (:uid)"), {"uid": uid_badge})
                        id_badge = conn.execute(text("SELECT id_badge FROM Badge WHERE uid_badge = :uid"), {"uid": uid_badge}).scalar()
                        id_employe = conn.execute(text("SELECT id_employe FROM Employe WHERE nom_employe = :nom_employe"), {"nom_employe": "Anonyme"}).scalar()
                        # Récupérer l'ID de l'alerte "Badge non attribué à un employé valide"
                        id_alerte = conn.execute(
                            text("SELECT id_alerte FROM Alerte WHERE message = :message"),
                            {"message": "Badge non attribué à un employé valide"}
                        ).scalar()
                        print("⚠️ UID inconnu, création d'un nouveau badge et utilisation des valeurs anonymes")

                # 🚀 Étape 4 : Récupérer les valeurs anonymes pour les autres colonnes
                id_equipe_anonyme = conn.execute(text("SELECT id_equipe FROM Equipe WHERE nom_equipe = :nom_equipe"), {"nom_equipe": "Équipe Anonyme"}).scalar()
                id_poste = conn.execute(text("SELECT id_poste FROM Poste_Competence WHERE nom_poste = :nom_poste"), {"nom_poste": "Poste Anonyme"}).scalar()
                id_emplacement_anonyme = conn.execute(text("SELECT id_emplacement FROM Emplacement WHERE nom_emplacement = :nom_emplacement"), {"nom_emplacement": "Emplacement Inconnu"}).scalar()

                # 🚀 Étape 5 : Gérer l'insertion ou la mise à jour selon le lecteur RFID
                if rfid_reader == 1:
                    # RFID1 : Insertion avec id_emplacement anonyme et date_entree = NULL
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
                        "id_equipe": id_equipe_anonyme,  # Utiliser l'ID d'équipe anonyme
                        "id_poste": id_poste,
                        "id_alerte": id_alerte,
                        "id_emplacement": id_emplacement_anonyme  # Utiliser l'ID d'emplacement anonyme
                    })
                    print("✅ Insertion dans la table Evenement réussie (RFID1)")  # Log de l'insertion réussie
                elif rfid_reader == 2:
                    # RFID2 : Mise à jour de date_entree, id_emplacement et id_equipe uniquement pour les UID autorisés
                    if id_alerte == conn.execute(
                        text("SELECT id_alerte FROM Alerte WHERE message = :message"),
                        {"message": "Accès accordé - Bienvenue !"}
                    ).scalar():  # Seulement si l'accès est autorisé
                        print("✅ Accès autorisé, vérification de l'équipe et du retard...")

                        # Récupérer l'équipe de l'employé
                        equipe_query = text("SELECT id_equipe FROM Employe WHERE id_employe = :id_employe")
                        id_equipe_employe = conn.execute(equipe_query, {"id_employe": id_employe}).scalar()
                        print(f"ID équipe employé : {id_equipe_employe}")

                        # Vérifier si l'employé est dans son intervalle d'équipe
                        heure_actuelle = datetime.now().time()
                        if est_dans_intervalle_equipe(heure_actuelle, id_equipe_employe):
                            print("✅ Employé dans son équipe, vérification du retard...")

                            # Calculer le retard
                            retard = calculer_retard(heure_actuelle, id_equipe_employe)
                            print(f"Retard calculé : {retard}")

                            if retard > timedelta(minutes=15):
                                # Récupérer l'ID de l'alerte "Retard de plus de 15 minutes"
                                id_alerte = conn.execute(
                                    text("SELECT id_alerte FROM Alerte WHERE message = :message"),
                                    {"message": "Retard de plus de 15 minutes"}
                                ).scalar()
                                print("⚠️ Employé en retard de plus de 15 minutes")
                            else:
                                # Récupérer l'ID de l'alerte "Accès accordé - Bienvenue !"
                                id_alerte = conn.execute(
                                    text("SELECT id_alerte FROM Alerte WHERE message = :message"),
                                    {"message": "Accès accordé - Bienvenue !"}
                                ).scalar()
                                print(f"✅ Employé dans son équipe, accès accordé")
                        else:
                            # Récupérer l'ID de l'alerte "Pas dans l'équipe appropriée"
                            id_alerte = conn.execute(
                                text("SELECT id_alerte FROM Alerte WHERE message = :message"),
                                {"message": "Pas dans l'équipe appropriée"}
                            ).scalar()
                            print("❌ Employé pas dans l'équipe appropriée")

                        # Mettre à jour la table Evenement
                        update_query = text("""
                            UPDATE Evenement
                            SET date_entree = :date_entree,
                                id_emplacement = :id_emplacement,
                                id_equipe = :id_equipe,
                                id_alerte = :id_alerte
                            WHERE id_badge = :id_badge AND date_entree IS NULL
                        """)
                        conn.execute(update_query, {
                            "date_entree": datetime.now(),
                            "id_emplacement": ID_EMPLACEMENT_RFID2,  # Utiliser l'ID d'emplacement fixe
                            "id_equipe": id_equipe_employe,  # Utiliser l'ID d'équipe de l'employé
                            "id_alerte": id_alerte,  # Mettre à jour l'alerte (retard ou accès accordé)
                            "id_badge": id_badge
                        })
                        print(f"✅ Mise à jour de la table Evenement avec id_alerte = {id_alerte}")  # Log de la mise à jour réussie
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