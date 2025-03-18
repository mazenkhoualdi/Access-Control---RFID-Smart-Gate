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
        return jsonify({"message": "Pas de donnees"}), 400

    print(f"Données reçues : {data}")  # Log des données reçues

    # Vérification des données
    uid_badge = data.get("uid_badge")
    rfid_reader = data.get("rfid_reader")  # Identifie quel lecteur RFID a été utilisé (1 ou 2)

    if not uid_badge or not rfid_reader:
        print("❌ UID ou lecteur RFID manquant")
        return jsonify({"message": " UID/RFID manq"}), 400

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
                        return jsonify({"message": " Acces refuse"}), 403
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
                    # RFID1 : Insertion ou mise à jour avec id_emplacement anonyme et date_entree = NULL
                    if id_employe:  # Seulement pour les employés non anonymes
                        # Vérifier si un enregistrement existe déjà pour cet employé
                        existing_event_query = text("""
                            SELECT id_event, date_entree, date_sortie FROM Evenement
                            WHERE id_employe = :id_employe
                        """)
                        existing_event = conn.execute(existing_event_query, {"id_employe": id_employe}).fetchone()

                        if existing_event:
                            id_event, date_entree, date_sortie = existing_event

                            if date_entree is not None and date_sortie is not None:
                                # L'employé a déjà un enregistrement complet (entrée et sortie), ne rien faire
                                print("✅ L'employé a déjà un enregistrement complet (entrée et sortie), aucune action nécessaire")
                                return jsonify({"message": "✅ Enreg. complet"}), 200
                            elif date_entree is not None and date_sortie is None:
                                # L'employé a déjà une entrée en cours, refuser une nouvelle entrée
                                print("❌ L'employé a déjà une entrée en cours (date_entree non nulle et date_sortie nulle)")
                                return jsonify({"message": " Entree en cours"}), 400
                            else:
                                # Mettre à jour l'enregistrement existant
                                update_query = text("""
                                    UPDATE Evenement
                                    SET date_entree = NULL,
                                        id_emplacement = :id_emplacement,
                                        id_equipe = :id_equipe,
                                        id_poste = :id_poste,
                                        id_alerte = :id_alerte
                                    WHERE id_event = :id_event
                                """)
                                conn.execute(update_query, {
                                    "id_emplacement": id_emplacement_anonyme,
                                    "id_equipe": id_equipe_anonyme,
                                    "id_poste": id_poste,
                                    "id_alerte": id_alerte,
                                    "id_event": id_event
                                })
                                print("✅ Mise à jour de l'enregistrement existant pour une nouvelle entrée")
                        else:
                            # Aucun enregistrement existant, insérer un nouvel enregistrement
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
                                "id_equipe": id_equipe_anonyme,
                                "id_poste": id_poste,
                                "id_alerte": id_alerte,
                                "id_emplacement": id_emplacement_anonyme
                            })
                            print("✅ Insertion dans la table Evenement réussie (RFID1)")
                    else:
                        # Pour les employés anonymes, insérer un nouvel enregistrement sans vérification
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
                            "id_equipe": id_equipe_anonyme,
                            "id_poste": id_poste,
                            "id_alerte": id_alerte,
                            "id_emplacement": id_emplacement_anonyme
                        })
                        print("✅ Insertion dans la table Evenement réussie (RFID1) pour un employé anonyme")

                elif rfid_reader == 2:
                    # RFID2 : Mise à jour de date_entree, id_emplacement, id_equipe et id_poste
                    if id_alerte == conn.execute(
                        text("SELECT id_alerte FROM Alerte WHERE message = :message"),
                        {"message": "Accès accordé - Bienvenue !"}
                    ).scalar():  # Seulement si l'accès est autorisé
                        print("✅ Accès autorisé, vérification de l'équipe et de la compétence...")

                        # Vérifier si l'employé a déjà badgé dans RFID2 (pour mettre à jour la date_sortie)
                        badge_rfid2_query = text("""
                            SELECT id_event FROM Evenement
                            WHERE id_badge = :id_badge AND date_entree IS NOT NULL AND date_sortie IS NULL
                        """)
                        badge_rfid2_result = conn.execute(badge_rfid2_query, {"id_badge": id_badge}).fetchone()

                        if badge_rfid2_result:
                            # Récupérer l'équipe de l'employé
                            equipe_query = text("SELECT id_equipe FROM Employe WHERE id_employe = :id_employe")
                            id_equipe_employe = conn.execute(equipe_query, {"id_employe": id_employe}).scalar()
                            print(f"ID équipe employé : {id_equipe_employe}")

                            # Vérifier si l'employé est dans son intervalle d'équipe
                            heure_actuelle = datetime.now().time()
                            if est_dans_intervalle_equipe(heure_actuelle, id_equipe_employe):
                                print("✅ L'employé est dans son intervalle d'équipe")

                                # Récupérer la compétence de l'employé
                                competence_employe_query = text("""
                                    SELECT competence FROM Employe WHERE id_employe = :id_employe
                                """)
                                competence_employe = conn.execute(competence_employe_query, {"id_employe": id_employe}).scalar()

                                # Récupérer la compétence associée à l'id_poste fixé sur RFID2
                                id_poste_rfid2 = 2  # ID du poste fixé sur RFID2
                                competence_poste_query = text("""
                                    SELECT competence FROM Poste_Competence WHERE id_poste = :id_poste
                                """)
                                competence_poste = conn.execute(competence_poste_query, {"id_poste": id_poste_rfid2}).scalar()

                                # Vérifier si la compétence de l'employé correspond à celle du poste RFID2
                                if competence_employe.strip().lower() == competence_poste.strip().lower():
                                    # Si la compétence correspond, mettre à jour la date_sortie
                                    update_sortie_query = text("""
                                        UPDATE Evenement
                                        SET date_sortie = :date_sortie
                                        WHERE id_badge = :id_badge AND date_entree IS NOT NULL AND date_sortie IS NULL
                                    """)
                                    conn.execute(update_sortie_query, {
                                        "date_sortie": datetime.now(),
                                        "id_badge": id_badge
                                    })
                                    print("✅ Date de sortie mise à jour dans la table Evenement")
                                    return jsonify({"message": "Sortie OK"}), 201
                                else:
                                    # Si la compétence ne correspond pas, refuser l'accès
                                    print("❌ Compétence non correspondante, date_sortie non mise à jour")
                                    return jsonify({"message": "Competence invalide"}), 403
                            else:
                                # Si l'employé n'est pas dans son intervalle d'équipe, refuser l'accès
                                print("❌ L'employé n'est pas dans son intervalle d'équipe")
                                return jsonify({"message": "Hors equipe"}), 403

                        # Vérifier si l'employé a déjà badgé dans RFID1
                        badge_rfid1_query = text("""
                            SELECT id_event FROM Evenement
                            WHERE id_badge = :id_badge AND date_entree IS NULL
                        """)
                        badge_rfid1_result = conn.execute(badge_rfid1_query, {"id_badge": id_badge}).fetchone()

                        if not badge_rfid1_result:
                            # Si l'employé n'a pas badgé dans RFID1, refuser l'accès
                            id_alerte = conn.execute(
                                text("SELECT id_alerte FROM Alerte WHERE message = :message"),
                                {"message": "Accès refusé - Badgeage RFID1 manquant"}
                            ).scalar()
                            print("❌ Accès refusé : l'employé n'a pas badgé dans RFID1")
                            return jsonify({"message": "RFID1 manquant"}), 403

                        # Récupérer l'équipe de l'employé
                        equipe_query = text("SELECT id_equipe FROM Employe WHERE id_employe = :id_employe")
                        id_equipe_employe = conn.execute(equipe_query, {"id_employe": id_employe}).scalar()
                        print(f"ID équipe employé : {id_equipe_employe}")

                        # Vérifier si l'employé est dans son intervalle d'équipe
                        heure_actuelle = datetime.now().time()
                        if est_dans_intervalle_equipe(heure_actuelle, id_equipe_employe):
                            print("✅ L'employé est dans son intervalle d'équipe")

                            # Récupérer la compétence de l'employé
                            competence_query = text("SELECT competence FROM Employe WHERE id_employe = :id_employe")
                            competence_employe = conn.execute(competence_query, {"id_employe": id_employe}).scalar()
                            print(f"Compétence de l'employé : {competence_employe}")

                            # Récupérer la compétence associée à l'id_poste 2
                            competence_poste_2_query = text("SELECT competence FROM Poste_Competence WHERE id_poste = 2")
                            competence_poste_2 = conn.execute(competence_poste_2_query).scalar()
                            print(f"Compétence requise pour id_poste 2 : {competence_poste_2}")

                            # Vérifier si la compétence de l'employé correspond à celle de l'id_poste 2
                            if competence_employe.strip().lower() == competence_poste_2.strip().lower():
                                # Si la compétence correspond et que l'employé est dans son équipe, mettre à jour la date_entree
                                update_query = text("""
                                    UPDATE Evenement
                                    SET date_entree = :date_entree,
                                        id_emplacement = :id_emplacement,
                                        id_equipe = :id_equipe,
                                        id_poste = :id_poste,
                                        id_alerte = :id_alerte
                                    WHERE id_badge = :id_badge AND date_entree IS NULL
                                """)
                                conn.execute(update_query, {
                                    "date_entree": datetime.now(),
                                    "id_emplacement": ID_EMPLACEMENT_RFID2,  # Utiliser l'ID d'emplacement fixe
                                    "id_equipe": id_equipe_employe,  # Utiliser l'ID d'équipe de l'employé
                                    "id_poste": 2,  # Mettre à jour l'id_poste à 2 (RFID2)
                                    "id_alerte": id_alerte,  # Mettre à jour l'alerte (accès accordé)
                                    "id_badge": id_badge
                                })
                                print(f"✅ Mise à jour de la table Evenement avec id_poste = 2 et id_alerte = {id_alerte}")
                                return jsonify({"message": "Entree OK"}), 201
                            else:
                                # Si la compétence ne correspond pas, refuser l'accès
                                print("❌ Compétence non correspondante, date_entree non enregistrée")
                                return jsonify({"message": "Competence invalide"}), 403
                        else:
                            # Si l'employé n'est pas dans son intervalle d'équipe, refuser l'accès
                            print("❌ L'employé n'est pas dans son intervalle d'équipe")
                            return jsonify({"message": "Hors equipe"}), 403
                    else:
                        print("❌ Badge non autorisé, mise à jour ignorée")
                        return jsonify({"message": "Acces refuse"}), 403

                # Vérifiez l'insertion ou la mise à jour
                verification_query = text("SELECT * FROM Evenement WHERE id_badge = :id_badge")
                verification_result = conn.execute(verification_query, {"id_badge": id_badge}).fetchone()
                print(f"Vérification de l'insertion/mise à jour : {verification_result}")  # Log de la vérification

                return jsonify({"message": "Enreg reussi"}), 201

    except Exception as e:
        print(f"❌ Erreur SQL : {str(e)}")  # Log des erreurs SQL
        return jsonify({"message": "Erreur SQL"}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)