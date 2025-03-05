USE SAGEMCOM_DB;

-- Table des employés --
CREATE TABLE Employe (
    id_employe INT PRIMARY KEY IDENTITY(1,1),
    nom_Employe VARCHAR(50) NOT NULL,
    prenom_Employe VARCHAR(50) NOT NULL
);

-- Table des équipes --
CREATE TABLE Equipe (
    id_equipe INT PRIMARY KEY IDENTITY(1,1),
    nom_Equipe VARCHAR(50) NOT NULL,
    CONSTRAINT unique_nom_Equipe UNIQUE (nom_Equipe)
);

-- Table des postes et compétences --
CREATE TABLE Poste_Competence (
    id_poste INT PRIMARY KEY IDENTITY(1,1),
    nom_poste VARCHAR(50) NOT NULL,
    competence VARCHAR(50) NOT NULL,
    etoiles INT NOT NULL CHECK (etoiles BETWEEN 1 AND 5)
);

-- Table des alertes --
CREATE TABLE Alerte (
    id_alerte INT PRIMARY KEY IDENTITY(1,1),
    message TEXT NOT NULL
);

-- Table des emplacements --
CREATE TABLE Emplacement (
    id_emplacement INT PRIMARY KEY IDENTITY(1,1),
    nom_emplacement VARCHAR(50) NOT NULL,
    type_emplacement VARCHAR(50) NOT NULL
);

-- Table des événements (sans description) --
CREATE TABLE Evenement (
    id_event INT PRIMARY KEY IDENTITY(1,1),
    id_employe INT NOT NULL,
    id_equipe INT NOT NULL,
    id_poste INT NOT NULL,
    id_alerte INT NOT NULL,
    id_emplacement INT NOT NULL,
    date_entree DATETIME NOT NULL,
    date_sortie DATETIME NULL,

    -- Clés étrangères pour assurer l'intégrité des relations
    FOREIGN KEY (id_employe) REFERENCES Employe(id_employe),
    FOREIGN KEY (id_equipe) REFERENCES Equipe(id_equipe),
    FOREIGN KEY (id_poste) REFERENCES Poste_Competence(id_poste),
    FOREIGN KEY (id_alerte) REFERENCES Alerte(id_alerte),
    FOREIGN KEY (id_emplacement) REFERENCES Emplacement(id_emplacement)
);

-- 1️Remplissage de la table Employe
INSERT INTO Employe (nom_Employe, prenom_Employe) VALUES 
('Ahmed', 'Ben Ali'), 
('Sara', 'Mansour'), 
('Mohamed', 'Trabelsi'), 
('Karim', 'Jlassi'), 
('Fatma', 'Dridi');

-- 2️ Remplissage de la table Equipe
INSERT INTO Equipe (nom_Equipe) VALUES 
('Développement'), 
('Support'), 
('Maintenance'), 
('Sécurité');

-- 3️ Remplissage de la table Poste_Competence
INSERT INTO Poste_Competence (nom_poste, competence, etoiles) VALUES 
('Développeur', 'Programmation', 4), 
('Technicien', 'Maintenance', 3), 
('Administrateur', 'Réseaux', 5), 
('Agent de Sécurité', 'Surveillance', 2), 
('Chef de Projet', 'Gestion', 5);

-- 4️ Remplissage de la table Alerte
INSERT INTO Alerte (message) VALUES 
('Bienvenue'), 
('Accès interdit'), 
('Retard détecté'), 
('Poste inadapté'), 
('Équipe inadéquate');

-- 5️ Remplissage de la table Emplacement
INSERT INTO Emplacement (nom_emplacement, type_emplacement) VALUES 
('Bureau A1', 'Bureau'), 
('Salle Serveur', 'Zone restreinte'), 
('Atelier de maintenance', 'Atelier'), 
('Entrée Principale', 'Contrôle d’accès'), 
('Open Space', 'Bureau');

--  Lier les employés à leurs équipes
-- Supposons que chaque employé ait une équipe différente
DECLARE @EquipeDev INT, @EquipeSupp INT, @EquipeMaint INT, @EquipeSec INT;
SELECT @EquipeDev = id_equipe FROM Equipe WHERE nom_Equipe = 'Développement';
SELECT @EquipeSupp = id_equipe FROM Equipe WHERE nom_Equipe = 'Support';
SELECT @EquipeMaint = id_equipe FROM Equipe WHERE nom_Equipe = 'Maintenance';
SELECT @EquipeSec = id_equipe FROM Equipe WHERE nom_Equipe = 'Sécurité';

-- 🔗 Lier les employés à leurs postes et compétences
DECLARE @PosteDev INT, @PosteTech INT, @PosteAdmin INT, @PosteSec INT, @PosteChef INT;
SELECT @PosteDev = id_poste FROM Poste_Competence WHERE nom_poste = 'Développeur';
SELECT @PosteTech = id_poste FROM Poste_Competence WHERE nom_poste = 'Technicien';
SELECT @PosteAdmin = id_poste FROM Poste_Competence WHERE nom_poste = 'Administrateur';
SELECT @PosteSec = id_poste FROM Poste_Competence WHERE nom_poste = 'Agent de Sécurité';
SELECT @PosteChef = id_poste FROM Poste_Competence WHERE nom_poste = 'Chef de Projet';

-- 🔗 Lier les employés à un emplacement
DECLARE @EmplacementBureau INT, @EmplacementServeur INT, @EmplacementAtelier INT, @EmplacementEntree INT, @EmplacementOpen INT;
SELECT @EmplacementBureau = id_emplacement FROM Emplacement WHERE nom_emplacement = 'Bureau A1';
SELECT @EmplacementServeur = id_emplacement FROM Emplacement WHERE nom_emplacement = 'Salle Serveur';
SELECT @EmplacementAtelier = id_emplacement FROM Emplacement WHERE nom_emplacement = 'Atelier de maintenance';
SELECT @EmplacementEntree = id_emplacement FROM Emplacement WHERE nom_emplacement = 'Entrée Principale';
SELECT @EmplacementOpen = id_emplacement FROM Emplacement WHERE nom_emplacement = 'Open Space';


