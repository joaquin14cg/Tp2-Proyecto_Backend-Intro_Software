SET NAMES utf8mb4;

USE club_deportivo;

CREATE TABLE deportes (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

INSERT INTO deportes (nombre)
VALUES
    ('Fútbol'),
    ('Tenis'),
    ('Pádel');