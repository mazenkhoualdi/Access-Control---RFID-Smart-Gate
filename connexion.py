import pandas as pd
from sqlalchemy import create_engine

#Paramètres de connexion
server = "DESKTOP-J50K35E\\SQLEXPRESS" 
database = "SAGEMCOM_DB"  

#Création de l'URL de connexion SQLAlchemy 
connection_string = f"mssql+pyodbc://@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"

#Création du moteur SQLAlchemy
engine = create_engine(connection_string)

#Vérification de la connexion
try:
    with engine.connect() as conn:
        print("✅ Connexion réussie à la base de données SQL Server.")
    

except Exception as e:
    print("❌ Erreur lors de la connexion :", e)
