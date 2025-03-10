from connexion import engine
import pandas as pd

def afficher_badges():
    try:
        query = "SELECT * FROM Badge"
        df = pd.read_sql(query, engine)
        print(df)
    except Exception as e:
        print("❌ Erreur lors de la récupération des badges :", e)
