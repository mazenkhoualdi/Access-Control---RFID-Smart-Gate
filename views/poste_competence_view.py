from connexion import engine
import pandas as pd

def afficher_postes():
    try:
        query = "SELECT * FROM Poste_Competence"
        df = pd.read_sql(query, engine)
        print(df)
    except Exception as e:
        print("❌ Erreur lors de la récupération des postes et compétences :", e)
