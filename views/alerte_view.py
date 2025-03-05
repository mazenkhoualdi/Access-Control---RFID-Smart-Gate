from connexion import engine
import pandas as pd

def afficher_alertes():
    try:
        query = "SELECT * FROM Alerte"
        df = pd.read_sql(query, engine)
        print(df)
    except Exception as e:
        print("❌ Erreur lors de la récupération des alertes :", e)
