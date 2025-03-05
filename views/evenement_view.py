from connexion import engine
import pandas as pd

def afficher_evenements():
    try:
        query = "SELECT * FROM Evenement"
        df = pd.read_sql(query, engine)
        print(df)
    except Exception as e:
        print("❌ Erreur lors de la récupération des événements :", e)
