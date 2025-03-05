from connexion import engine
import pandas as pd

def afficher_emplacements():
    try:
        query = "SELECT * FROM Emplacement"
        df = pd.read_sql(query, engine)
        print(df)
    except Exception as e:
        print("❌ Erreur lors de la récupération des emplacements :", e)
