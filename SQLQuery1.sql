USE SAGEMCOM_DB;

-- Table des équipes --
CREATE TABLE Equipe (
    id_equipe INT PRIMARY KEY IDENTITY(1,1),
    nom_equipe VARCHAR(50) NOT NULL UNIQUE
);

-- Table des employés --
CREATE TABLE Employe (
    id_employe INT PRIMARY KEY IDENTITY(1,1),
    nom_employe VARCHAR(50) NOT NULL,
    prenom_employe VARCHAR(50) NOT NULL,
    id_equipe INT NOT NULL,
    competence VARCHAR(50) NOT NULL,
    FOREIGN KEY (id_equipe) REFERENCES Equipe(id_equipe)
);

-- Table des badges (pour une meilleure gestion) --
CREATE TABLE Badge (
    id_badge INT PRIMARY KEY IDENTITY(1,1),
    uid_badge VARCHAR(50) UNIQUE NOT NULL,
    id_employe INT NULL, -- NULL si badge non attribué
    FOREIGN KEY (id_employe) REFERENCES Employe(id_employe) ON DELETE SET NULL
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
    message VARCHAR(255) NOT NULL
);

-- Table des emplacements --
CREATE TABLE Emplacement (
    id_emplacement INT PRIMARY KEY IDENTITY(1,1),
    nom_emplacement VARCHAR(50) NOT NULL,
    type_emplacement VARCHAR(50) NOT NULL
);

-- Table des événements --
CREATE TABLE Evenement (
    id_event INT PRIMARY KEY IDENTITY(1,1),
    id_employe INT NULL, -- NULL si badge inconnu
    id_badge INT NOT NULL, -- On stocke l'id_badge ici
    id_equipe INT NOT NULL,
    id_poste INT NOT NULL,
    id_alerte INT NULL, -- Peut être NULL si aucun problème
    id_emplacement INT NOT NULL,
    date_entree DATETIME  NULL,
    date_sortie DATETIME NULL,
    -- Clés étrangères
    FOREIGN KEY (id_employe) REFERENCES Employe(id_employe) ON DELETE SET NULL,
    FOREIGN KEY (id_badge) REFERENCES Badge(id_badge),
    FOREIGN KEY (id_equipe) REFERENCES Equipe(id_equipe),
    FOREIGN KEY (id_poste) REFERENCES Poste_Competence(id_poste),
    FOREIGN KEY (id_alerte) REFERENCES Alerte(id_alerte),
    FOREIGN KEY (id_emplacement) REFERENCES Emplacement(id_emplacement)
);
-- Insérer des équipes
-- Insérer des équipes
INSERT INTO Equipe (nom_equipe)
VALUES 
    ('Équipe 1 - 6h à 14h'),  -- Première équipe (6h-14h)
    ('Équipe 2 - 14h à 22h'), -- Deuxième équipe (14h-22h)
    ('Équipe 3 - 22h à 6h');  -- Troisième équipe (22h-6h)

	-- Insérer des employés
INSERT INTO Employe (nom_employe, prenom_employe, id_equipe, competence)
VALUES 
    ('Doe', 'John', 1, 'Développement logiciel'), 
    ('Smith', 'Jane', 2, 'Maintenance système'),
    ('Brown', 'Alex', 3, 'Gestion de projet'),
    ('Taylor', 'Sam', 1, 'Gestion de réseau'),
    ('Miller', 'Chris', 2, 'Maintenance système');  -- Employé pour la deuxième équipe
	-- Insérer des badges attribués aux employés
INSERT INTO Badge (uid_badge, id_employe)
VALUES 
    ('63F5B428', 1),  -- Badge 1 attribué à l'employé 1
    ('C5D5963F', 2),  -- Badge 2 attribué à l'employé 2
    ('4A19044B', 3),  -- Badge 3 attribué à l'employé 3
    ('F1A3707B', 4),  -- Badge 4 attribué à l'employé 4
    ('B38838DA', 7);  -- Badge anonyme, pas d'employé attribué (id_employe NULL)
-- Insérer des postes avec compétences
INSERT INTO Poste_Competence (nom_poste, competence, etoiles)
VALUES 
    ('Développeur', 'Développement logiciel', 5),   -- Poste de développeur avec compétence "Développement logiciel" et 5 étoiles
    ('Technicien', 'Maintenance système', 4),       -- Poste de technicien avec compétence "Maintenance système" et 4 étoiles
    ('Manager', 'Gestion de projet', 3),            -- Poste de manager avec compétence "Gestion de projet" et 3 étoiles
    ('Administrateur', 'Gestion de réseau', 4);     -- Poste d'administrateur avec compétence "Gestion de réseau" et 4 étoiles
-- Insérer des emplacements
INSERT INTO Emplacement (nom_emplacement, type_emplacement)
VALUES 
    ('Entrée principale', 'Accès à lentreprise'),
    ('Poste de travail A', 'Bureau'),
    ('Poste de travail B', 'Bureau'),
    ('Salle serveur', 'Salle technique');
-- Insérer des alertes dans la table Alerte
INSERT INTO Alerte (message)
VALUES 
    ('Accès non autorisé - Badge invalide'),
    ('Retard dentrée - Plus de 15 minutes'),
    ('Compétence incorrecte pour ce poste'),
    ('Emplacement incorrect pour léquipe'),
    ('Badge non attribué à un employé valide'),
    ('Accès accordé - Bienvenue !'),
    ('Accès autorisé - Compétence validée');



	-- 🔹 Insérer une équipe anonyme
INSERT INTO Equipe (nom_equipe) 
VALUES ('Équipe Anonyme');
INSERT INTO Employe (nom_employe, prenom_employe, id_equipe, competence)
VALUES ('Anonyme', 'Employe', (SELECT id_equipe FROM Equipe WHERE nom_equipe = 'Équipe Anonyme'), 'Inconnu');
INSERT INTO Poste_Competence (nom_poste, competence, etoiles)
VALUES ('Poste Anonyme', 'Inconnu', 1);
INSERT INTO Emplacement (nom_emplacement, type_emplacement)
VALUES ('Emplacement Inconnu', 'Inconnu');
