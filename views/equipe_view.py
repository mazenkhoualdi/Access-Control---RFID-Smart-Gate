from connexion import engine
import pandas as pd

def afficher_equipes():
    try:
        query = "SELECT * FROM Equipe"
        df = pd.read_sql(query, engine)
        print(df)
    except Exception as e:
        print("❌ Erreur lors de la récupération des équipes :", e)
