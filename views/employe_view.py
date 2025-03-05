from connexion import engine
import pandas as pd

def afficher_employes():
    try:
        query = "SELECT * FROM Employe"
        df = pd.read_sql(query, engine)
        print(df)
    except Exception as e:
        print("❌ Erreur lors de la récupération des employés :", e)
