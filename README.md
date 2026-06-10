# Sagemcom-RFID-Access-Control

**Système de Contrôle d'Accès Intelligent par Badges RFID**

Projet de Fin d'Études (PFE) - Stage Ingénieur chez Sagemcom

---

## 📋 Description

Ce projet consiste en la conception et la réalisation d'un **système de contrôle d'accès sécurisé** basé sur la technologie RFID à double lecteur.

Le système permet de :
- Gérer l'entrée et la sortie des employés via deux lecteurs RFID
- Vérifier en temps réel les horaires d'équipe, les compétences et les accès autorisés
- Enregistrer tous les événements dans une base de données SQL Server
- Afficher des alertes et des messages sur un écran LCD
- Contrôler des LEDs RGB pour indication visuelle (Vert = Autorisé, Rouge = Refusé, Bleu = Erreur)

---

## 🛠️ Technologies Utilisées

### Hardware
- **Microcontrôleur** : ESP32
- **Lecteurs RFID** : 2 × MFRC522
- **Affichage** : LCD 16x2 avec interface I2C
- **Indication visuelle** : LEDs RGB
- **Connexion** : WiFi

### Software
- **Backend** : Python + Flask
- **Base de données** : Microsoft SQL Server
- **ORM** : SQLAlchemy
- **Microcontrôleur** : Arduino C++
- **Communication** : JSON via HTTP POST
- **Administration** : Interface console Python (Pandas)

---

## 📁 Structure du Projet
Sagemcom-RFID-Access-Control/
├── ArduinoIDE_File.txt          # Code source Arduino pour ESP32
├── server.py                    # API Flask principale
├── main.py                      # Menu d'administration
├── connexion.py                 # Connexion à la base de données
├── SQLQuery1.sql                # Script création base + données de test
├── models/                      # Modèles SQLAlchemy
├── views/                       # Vues console d'affichage
├── example.db                   # Base de test SQLite
└── README.md
text---

## 🚀 Installation et Lancement

### 1. Base de données

Exécutez le script `SQLQuery1.sql` sur **SQL Server** pour créer la base `SAGEMCOM_DB` et insérer les données de test.

### 2. Environnement Python

```bash
# Création de l'environnement virtuel
python -m venv venv

# Activation (Windows)
venv\Scripts\activate

# Installation des dépendances
pip install flask sqlalchemy pandas pyodbc
3. Configuration
Modifiez les informations de connexion dans les fichiers :

connexion.py
server.py

Exemple :
Pythonserver = "DESKTOP-J50K35E\\SQLEXPRESS"
database = "SAGEMCOM_DB"
4. Arduino (ESP32)

Ouvrir ArduinoIDE_File.txt dans l’Arduino IDE
Modifier le SSID et mot de passe WiFi
Mettre à jour l’URL du serveur (serverUrl)
Téléverser le code sur l’ESP32

5. Lancement
Bash# Terminal 1 - Lancer le serveur Flask
python server.py

# Terminal 2 - Lancer l'interface d'administration
python main.py

🔑 Fonctionnalités Principales

Double lecteur RFID (Entrée / Poste de travail)
Vérification automatique des horaires d’équipe
Contrôle des compétences par poste
Gestion des badges anonymes et spéciaux
Enregistrement des entrées/sorties avec horodatage
Feedback instantané via LCD et LEDs
Protection contre les doubles scans


📊 Données de Test
Badges disponibles :



































UIDNomÉquipePoste63F5B428John DoeÉquipe 1DéveloppeurC5D5963FJane SmithÉquipe 2Technicien4A19044BAlex BrownÉquipe 3ManagerANONYME0AnonymeÉquipe Anonyme-

🎯 Améliorations Futures

Interface web (Dashboard administrateur)
Notifications email/SMS
Statistiques de présence et retards
Support QR Code + NFC
Application mobile


👨‍💻 Auteur
Projet PFE - Stage Sagemcom
Développé par [Votre Nom]

📄 Licence
Projet académique - Tous droits réservés © 2026
text**Vous pouvez maintenant copier tout le contenu ci-dessus et le coller dans un fichier nommé `README.md`** à la racine de votre projet.
