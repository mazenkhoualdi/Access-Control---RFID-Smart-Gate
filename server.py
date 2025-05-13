from flask import Flask, request, jsonify
from sqlalchemy import create_engine, text
from datetime import datetime, timedelta

app = Flask(__name__)

# Configuration de la base de données
server = "DESKTOP-J50K35E\\SQLEXPRESS"
database = "SAGEMCOM_DB"
connection_string = f"mssql+pyodbc://@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
engine = create_engine(connection_string)

# Constantes métiers
ID_EMPLACEMENT_RFID2 = 4
ID_POSTE_ANONYME = 5
ID_POSTE_TECHNICIEN = 2
DELAI_RETARD = timedelta(minutes=15)
EMPLOYE_SPECIAL = "B38838DA"  # Employé spécial

# Configuration des équipes
HEURES_DEBUT_EQUIPE = {
    1: datetime.strptime("06:00:00", "%H:%M:%S").time(),
    2: datetime.strptime("14:00:00", "%H:%M:%S").time(),
    3: datetime.strptime("22:00:00", "%H:%M:%S").time(),
}
DUREE_EQUIPE = timedelta(hours=8)

# Fonctions utilitaires
def get_id_poste(conn, nom_poste, default_id):
    """Récupère l'ID d'un poste par son nom ou retourne l'ID par défaut"""
    result = conn.execute(
        text("SELECT id_poste FROM Poste_Competence WHERE nom_poste = :nom_poste"),
        {"nom_poste": nom_poste}
    ).fetchone()
    return result[0] if result else default_id

def est_dans_intervalle_equipe(heure_actuelle, id_equipe):
    debut_equipe = HEURES_DEBUT_EQUIPE.get(id_equipe)
    if not debut_equipe:
        return False

    debut_equipe_dt = datetime.combine(datetime.today(), debut_equipe)
    fin_equipe_dt = debut_equipe_dt + DUREE_EQUIPE
    heure_actuelle_dt = datetime.combine(datetime.today(), heure_actuelle)

    if heure_actuelle_dt < debut_equipe_dt:
        heure_actuelle_dt += timedelta(days=1)

    return debut_equipe_dt <= heure_actuelle_dt < fin_equipe_dt

def get_alert_id(conn, message):
    result = conn.execute(
        text("SELECT id_alerte FROM Alerte WHERE message = :message"),
        {"message": message}
    ).fetchone()
    return result[0] if result else None

def ensure_alerts_exist(conn):
    alerts = {
        "Badge invalide": 1,
        "retard plus de 15 minutes": 2,
        "Competence incorrecte": 3,
        "Hors équipe": 4,
        "Badge non attribue": 5,
        "Bienvenue !": 6
    }

def est_badge_anonyme_ou_special(conn, uid_badge):
    """Vérifie si le badge est l'employé spécial ou un badge anonyme non défini"""
    if uid_badge == EMPLOYE_SPECIAL:
        return True
    
    # Vérifie si le badge n'existe pas dans la table Employe
    result = conn.execute(
        text("SELECT 1 FROM Employe WHERE id_employe = :uid"),
        {"uid": uid_badge}
    ).fetchone()
    return result is None

def verifier_un_seul_enregistrement(conn, id_employe):
    """Vérifie qu'un employé n'a qu'un seul enregistrement complet sauf pour badges spéciaux/anonymes"""
    if est_badge_anonyme_ou_special(conn, id_employe):
        return True  # Les badges spéciaux/anonymes peuvent avoir plusieurs enregistrements
    
    count = conn.execute(
        text("""
            SELECT COUNT(*) FROM Evenement 
            WHERE id_employe = :id_employe 
            AND date_sortie IS NOT NULL
        """),
        {"id_employe": id_employe}
    ).scalar()
    return count == 0

# Points d'entrée API
@app.route('/evenement', methods=['POST'])
def handle_event():
    data = request.get_json()
    if not data:
        return jsonify({"message": "Pas de données"}), 400

    uid_badge = data.get("uid_badge")
    rfid_reader = data.get("rfid_reader")

    if not uid_badge or not rfid_reader:
        return jsonify({"message": "RFID manquant"}), 400

    try:
        with engine.connect() as conn:
            with conn.begin():
                ensure_alerts_exist(conn)

                # Vérification si le badge est spécial/anonyme
                if est_badge_anonyme_ou_special(conn, uid_badge):
                    if rfid_reader == 1:
                        return handle_badge_special_ou_anonyme(conn, uid_badge)
                    else:
                        return jsonify({
                            "message": "Badge non permis",
                            "id_alerte": 1  # Badge invalide
                        }), 403

                if rfid_reader == 1:
                    return handle_rfid1(conn, uid_badge)
                elif rfid_reader == 2:
                    return handle_rfid2(conn, uid_badge)

    except Exception as e:
        print(f"Erreur: {str(e)}")
        return jsonify({"message": f"Erreur serveur: {str(e)}"}), 500

def handle_badge_special_ou_anonyme(conn, uid_badge):
    """Gestion spéciale pour les badges spéciaux/anonymes"""
    # On insère toujours une nouvelle entrée sans vérifier les sorties
    id_poste = get_id_poste(conn, 'Post_anonyme', ID_POSTE_ANONYME)
    id_emplacement = conn.execute(
        text("SELECT id_emplacement FROM Emplacement WHERE nom_emplacement = 'Entrée principale'")
    ).scalar()

    conn.execute(
        text("""
            INSERT INTO Evenement (
                id_employe, id_poste, id_alerte, 
                id_emplacement, date_entree
            ) VALUES (
                :id, :poste, :alerte, 
                :emplacement, :now
            )
        """),
        {
            "id": uid_badge,
            "poste": id_poste,
            "alerte": 1,  # Toujours Badge invalide
            "emplacement": id_emplacement,
            "now": datetime.now()
        }
    )
    return jsonify({
        "message": "badge anonyme",
        "id_alerte": 1  # Badge invalide
    }), 201

def verifier_un_seul_enregistrement(conn, id_employe):
    """Vérifie qu'un employé n'a qu'un seul enregistrement complet par jour sauf pour badges spéciaux/anonymes"""
    if est_badge_anonyme_ou_special(conn, id_employe):
        return True  # Les badges spéciaux/anonymes peuvent avoir plusieurs enregistrements
    
    today = datetime.now().date()
    count = conn.execute(
        text("""
            SELECT COUNT(*) FROM Evenement 
            WHERE id_employe = :id_employe 
            AND date_sortie IS NOT NULL
            AND CAST(date_entree AS DATE) = :today
        """),
        {"id_employe": id_employe, "today": today}
    ).scalar()
    return count == 0

def handle_rfid1(conn, uid_badge):
    employe_info = conn.execute(
        text("SELECT id_employe, nom_employe, id_equipe FROM Employe WHERE id_employe = :uid"),
        {"uid": uid_badge}
    ).fetchone()

    if employe_info:
        id_employe, nom_employe, id_equipe = employe_info
        alerte_id = get_alert_id(conn, "Bienvenue !") or 6
        
        if not verifier_un_seul_enregistrement(conn, id_employe):
            return jsonify({
                "message": "Deja scanne aujourd'hui",
                "id_alerte": alerte_id
            }), 400
    else:
        # Cas normalement déjà géré par est_badge_anonyme_ou_special
        return handle_badge_special_ou_anonyme(conn, uid_badge)

    # Vérifier s'il y a une entrée non fermée aujourd'hui
    today = datetime.now().date()
    event = conn.execute(
        text("""
            SELECT id_event FROM Evenement 
            WHERE id_employe = :id 
            AND date_sortie IS NULL
            AND CAST(date_entree AS DATE) = :today
        """),
        {"id": id_employe, "today": today}
    ).fetchone()

    if event:
        conn.execute(
            text("UPDATE Evenement SET date_sortie = :now WHERE id_event = :id"),
            {"now": datetime.now(), "id": event[0]}
        )
        return jsonify({"message": "Sortie enregistree"}), 200
    else:
        id_poste = get_id_poste(conn, 'Post_anonyme', ID_POSTE_ANONYME)
        id_emplacement = conn.execute(
            text("SELECT id_emplacement FROM Emplacement WHERE nom_emplacement = 'Entrée principale'")
        ).scalar()

        conn.execute(
            text("""
                INSERT INTO Evenement (
                    id_employe, id_poste, id_alerte, 
                    id_emplacement, date_entree
                ) VALUES (
                    :id, :poste, :alerte, 
                    :emplacement, :now
                )
            """),
            {
                "id": id_employe,
                "poste": id_poste,
                "alerte": alerte_id,
                "emplacement": id_emplacement,
                "now": datetime.now()
            }
        )
        return jsonify({"message": "Entree enregistree"}), 201
    employe_info = conn.execute(
        text("SELECT id_employe, nom_employe, id_equipe FROM Employe WHERE id_employe = :uid"),
        {"uid": uid_badge}
    ).fetchone()

    if employe_info:
        id_employe, nom_employe, id_equipe = employe_info
        alerte_id = get_alert_id(conn, "Bienvenue !") or 6
        
        if not verifier_un_seul_enregistrement(conn, id_employe):
            return jsonify({
                "message": "Deja scanne",
                "id_alerte": alerte_id
            }), 400
    else:
        # Cas normalement déjà géré par est_badge_anonyme_ou_special
        return handle_badge_special_ou_anonyme(conn, uid_badge)

    event = conn.execute(
        text("SELECT id_event FROM Evenement WHERE id_employe = :id AND date_sortie IS NULL"),
        {"id": id_employe}
    ).fetchone()

    if event:
        conn.execute(
            text("UPDATE Evenement SET date_sortie = :now WHERE id_event = :id"),
            {"now": datetime.now(), "id": event[0]}
        )
        return jsonify({"message": "Sortie enregistree"}), 200
    else:
        id_poste = get_id_poste(conn, 'Post_anonyme', ID_POSTE_ANONYME)
        id_emplacement = conn.execute(
            text("SELECT id_emplacement FROM Emplacement WHERE nom_emplacement = 'Entrée principale'")
        ).scalar()

        conn.execute(
            text("""
                INSERT INTO Evenement (
                    id_employe, id_poste, id_alerte, 
                    id_emplacement, date_entree
                ) VALUES (
                    :id, :poste, :alerte, 
                    :emplacement, :now
                )
            """),
            {
                "id": id_employe,
                "poste": id_poste,
                "alerte": alerte_id,
                "emplacement": id_emplacement,
                "now": datetime.now()
            }
        )
        return jsonify({"message": "Entree enregistree"}), 201

def handle_rfid2(conn, uid_badge):
    employe_info = conn.execute(
        text("""
            SELECT E.id_employe, E.id_equipe, E.competence, PC.id_poste
            FROM Employe E
            JOIN Poste_Competence PC ON E.competence = PC.competence
            WHERE E.id_employe = :uid
        """),
        {"uid": uid_badge}
    ).fetchone()

    if not employe_info:
        return jsonify({
            "message": "Employe non trouve",
            "id_alerte": get_alert_id(conn, "Badge non attribue") or 5
        }), 400

    id_employe, id_equipe, competence_employe, id_poste_employe = employe_info

    event = conn.execute(
        text("SELECT id_event FROM Evenement WHERE id_employe = :id AND date_sortie IS NULL"),
        {"id": id_employe}
    ).fetchone()

    if not event:
        return jsonify({
            "message": "Entree absente",
            "id_alerte": get_alert_id(conn, "Bienvenue !") or 6
        }), 400

    competence_requise = conn.execute(
        text("SELECT competence FROM Poste_Competence WHERE id_poste = :poste"),
        {"poste": ID_POSTE_TECHNICIEN}
    ).scalar()

    alerte_id = None
    access_autorise = True
    details = {}

    heure_actuelle = datetime.now().time()
    if not est_dans_intervalle_equipe(heure_actuelle, id_equipe):
        alerte_id = get_alert_id(conn, "Hors équipe") or 4
        access_autorise = False
        details["hors_intervalle"] = True

    if access_autorise:
        if not competence_requise or competence_employe.lower().strip() != competence_requise.lower().strip():
            alerte_id = get_alert_id(conn, "Competence incorrecte") or 3
            access_autorise = False
            details["competence_invalide"] = True
        else:
            alerte_id = get_alert_id(conn, "Bienvenue !") or 6

    conn.execute(
        text("""
            UPDATE Evenement SET
                id_poste = :poste,
                id_emplacement = :emplacement,
                id_alerte = :alerte
            WHERE id_event = :id
        """),
        {
            "poste": id_poste_employe,
            "emplacement": ID_EMPLACEMENT_RFID2,
            "alerte": alerte_id,
            "id": event[0]
        }
    )

    if not access_autorise:
    # Récupérer le message d'alerte pour l'id_alerte depuis la table Evenement
        alerte_message = conn.execute(
            text("""
                SELECT A.message 
                FROM Alerte A
                WHERE A.id_alerte = :alerte_id
            """),
            {"alerte_id": alerte_id}
        ).scalar()

    # Utiliser le message récupéré ou un message par défaut
        return jsonify({
            "message": alerte_message or "Acces refuse",
            "id_alerte": alerte_id,
            "details": details
        }), 403
    return jsonify({
        "message": "Acces autorise",
        "id_alerte": alerte_id
    }), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)