from views.employe_view import afficher_employes
from views.equipe_view import afficher_equipes
from views.poste_competence_view import afficher_postes
from views.alerte_view import afficher_alertes
from views.emplacement_view import afficher_emplacements
from views.evenement_view import afficher_evenements

# Menu principal
def main():
    while True:
        print("\n📌 Menu Principal")
        print("1️⃣ - Afficher les employés")
        print("2️⃣ - Afficher les équipes")
        print("3️⃣ - Afficher les postes et compétences")
        print("4️⃣ - Afficher les alertes")
        print("5️⃣ - Afficher les emplacements")
        print("6️⃣ - Afficher les événements")
        print("0️⃣ - Quitter")

        choix = input("Choisissez une option : ")

        if choix == "1":
            afficher_employes()
        elif choix == "2":
            afficher_equipes()
        elif choix == "3":
            afficher_postes()
        elif choix == "4":
            afficher_alertes()
        elif choix == "5":
            afficher_emplacements()
        elif choix == "6":
            afficher_evenements()
        elif choix == "0":
            print("👋 Au revoir !")
            break
        else:
            print("❌ Option invalide, essayez encore.")

if __name__ == "__main__":
    main()
