CREATE TABLE IF NOT EXISTS agences (
	id_agence INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	ville VARCHAR(30) COLLATE UTF8mb4_UNICODE_CI,
	dirigeant VARCHAR(30) COLLATE UTF8mb4_UNICODE_CI,
	flotte INT
)
ENGINE = InnoDB;


CREATE TABLE IF NOT EXISTS voitures(
	id_voiture INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	id_agence INT NOT NULL,
	constructeur VARCHAR(30) COLLATE UTF8mb4_UNICODE_CI,
	annee INT,
	carburant VARCHAR(30) COLLATE UTF8mb4_UNICODE_CI,
	FOREIGN KEY(id_agence) REFERENCES Agences(id_agence)
)
ENGINE = INNODB;


INSERT INTO agences(ville,dirigeant,flotte) VALUES
	("Paris_I","Dupont",55),
	("Lyon","Ferrière",82),
	("Paris_XII","Dupont",103),
	("Bordeaux","Durand",41),
	("Tours","Bertrand",39);