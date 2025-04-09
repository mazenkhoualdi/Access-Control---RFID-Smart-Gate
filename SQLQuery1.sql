USE SAGEMCOM_DB;
-- Table des équipes --
CREATE TABLE Equipe (
    id_equipe INT PRIMARY KEY IDENTITY(1,1),
    nom_equipe VARCHAR(50) NOT NULL UNIQUE -- Le `UNIQUE` est maintenant correctement placé à la fin
);

   

-- Table des employés --
CREATE TABLE Employe (
    id_employe VARCHAR(50) PRIMARY KEY,  -- Utilisation de VARCHAR au lieu de INT
    nom_employe VARCHAR(50) NOT NULL,
    prenom_employe VARCHAR(50) NOT NULL,
    id_equipe INT NOT NULL,
    competence VARCHAR(50) NOT NULL,
    FOREIGN KEY (id_equipe) REFERENCES Equipe(id_equipe)
);


-- Table des postes et compétences --
CREATE TABLE Poste_Competence (
    id_poste INT PRIMARY KEY IDENTITY(1,1),
    nom_poste VARCHAR(50) NOT NULL,
    competence VARCHAR(50) NOT NULL,
    etoiles INT NOT NULL CHECK (etoiles BETWEEN 1 AND 5),


);

-- Table des alertes --
CREATE TABLE Alerte (
    id_alerte INT PRIMARY KEY IDENTITY(1,1),
    message TEXT NOT NULL
);
ALTER TABLE Alerte ALTER COLUMN message NVARCHAR(MAX);
-- Table des emplacements --
CREATE TABLE Emplacement (
    id_emplacement INT PRIMARY KEY IDENTITY(1,1),
    nom_emplacement VARCHAR(50) NOT NULL,
    type_emplacement VARCHAR(50) NOT NULL
);

-- Table des événements --
CREATE TABLE Evenement (
    id_event INT PRIMARY KEY IDENTITY(1,1),
    id_employe VARCHAR(50) NOT NULL, 
    id_poste INT NOT NULL,
    id_alerte INT NOT NULL, 
    id_emplacement INT NOT NULL,
    date_entree DATETIME NOT NULL,
    date_sortie DATETIME NULL,
    -- Clés étrangères
    FOREIGN KEY (id_employe) REFERENCES Employe(id_employe) ,
    FOREIGN KEY (id_poste) REFERENCES Poste_Competence(id_poste),
    FOREIGN KEY (id_alerte) REFERENCES Alerte(id_alerte),
    FOREIGN KEY (id_emplacement) REFERENCES Emplacement(id_emplacement)
);
ALTER TABLE Evenement
ALTER COLUMN id_employe VARCHAR(50) NOT NULL;

ALTER TABLE Evenement
ALTER COLUMN id_alerte INT NOT NULL;

-- Insérer des équipes
INSERT INTO Equipe (nom_equipe)
VALUES
    ('Équipe 1 - 6h à 14h'),  -- Première équipe (6h-14h)
    ('Équipe 2 - 14h à 22h'), -- Deuxième équipe (14h-22h)
    ('Équipe 3 - 22h à 6h'), -- Troisième équipe (22h-6h)
('Equipe_anonyme');

-- Insérer des employés
-- Comme `id_employe` est une clé primaire avec `IDENTITY`, il n'est pas nécessaire de spécifier une valeur pour cette colonne.
-- Les IDs seront générés automatiquement.

INSERT INTO Employe (id_employe, nom_employe, prenom_employe, id_equipe, competence)
VALUES
    ('63F5B428', 'Doe', 'John', 1, 'Développeur'),
    ('C5D5963F', 'Smith', 'Jane', 2, 'Technicien'),
    ('4A19044B', 'Brown', 'Alex', 3, 'Manager'),
    ('F1A3707B', 'Taylor', 'Sam', 1, 'Administrateur'),
    ('B38838DA', 'Miller', 'Chris', 2, 'Technicien'),
('ANONYME0','anonyme','anonyme',4,'inconnue');


-- Insérer des postes et compétences
INSERT INTO Poste_Competence (nom_poste, competence, etoiles)
VALUES
    ('Développeur', 'Développement logiciel', 5),   -- Poste de développeur avec compétence "Développement logiciel" et 5 étoiles
    ('Technicien', 'Maintenance système', 4),       -- Poste de technicien avec compétence "Maintenance système" et 4 étoiles
    ('Manager', 'Gestion de projet', 3),            -- Poste de manager avec compétence "Gestion de projet" et 3 étoiles
    ('Administrateur', 'Gestion de réseau', 4),    -- Poste d'administrateur avec compétence "Gestion de réseau" et 4 étoiles
('Post_anonyme','inconnue',1);

-- Insérer des emplacements
INSERT INTO Emplacement (nom_emplacement, type_emplacement)
VALUES
    ('Entrée principale', 'Accès à lentreprise'),
    ('Poste de travail A', 'Bureau'),
    ('Poste de travail B', 'Bureau'),
    ('Salle serveur', 'Salle technique');

-- Insérer des alertes
INSERT INTO Alerte (message)
VALUES
    ('Badge invalide'),
    ('retard plus de 15 minutes'),
    ('Competence incorrecte'),
    ('Emplacement incorrect'),
    ('Badge non attribue'),
    ('Bienvenue !'),
    ('Competence valide');

-- Sélectionner les événements
select * from equipe;
select * from Poste_Competence
select * from Employe
select * from Alerte
select * from Emplacement
select * from Evenement
