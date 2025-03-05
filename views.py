from models import session, Employe, Equipe, PosteCompetence, Alerte, Emplacement, Evenement

# Afficher tous les employés
def afficher_employes():
    employes = session.query(Employe).all()
    for emp in employes:
        print(f"ID: {emp.id_employe}, Nom: {emp.nom_Employe}, Prénom: {emp.prenom_Employe}")

# Afficher toutes les équipes
def afficher_equipes():
    equipes = session.query(Equipe).all()
    for eq in equipes:
        print(f"ID: {eq.id_equipe}, Nom: {eq.nom_Equipe}")

# Afficher tous les postes
def afficher_postes():
    postes = session.query(PosteCompetence).all()
    for poste in postes:
        print(f"ID: {poste.id_poste}, Poste: {poste.nom_poste}, Compétence: {poste.competence}, Niveau: {poste.etoiles}")

# Afficher les alertes
def afficher_alertes():
    alertes = session.query(Alerte).all()
    for alerte in alertes:
        print(f"ID: {alerte.id_alerte}, Message: {alerte.message}")

# Afficher tous les emplacements
def afficher_emplacements():
    emplacements = session.query(Emplacement).all()
    for emp in emplacements:
        print(f"ID: {emp.id_emplacement}, Nom: {emp.nom_emplacement}, Type: {emp.type_emplacement}")

# Afficher les événements
def afficher_evenements():
    evenements = session.query(Evenement).all()
    for event in evenements:
        print(f"ID Event: {event.id_event}, Employé: {event.id_employe}, Date entrée: {event.date_entree}, Date sortie: {event.date_sortie}")

