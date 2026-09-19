SET NAMES utf8mb4; -- sirve para trabajar con caracteres tipo ú

USE club_deportivo;

DROP TABLE IF EXISTS reservas;
DROP TABLE IF EXISTS socios;
DROP TABLE IF EXISTS canchas;
DROP TABLE IF EXISTS deportes;

CREATE TABLE deportes (
    id  INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci; -- character set define cómo se almacenan los caracteres especiales como tildes y ñ, y collation define cómo se comparan y ordenan esos caracteres (no distingue entre mayúsculas y minúsculas).

INSERT INTO deportes (nombre)
VALUES
    ('Fútbol'),
    ('Tenis'),
    ('Pádel');

CREATE TABLE canchas (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    deporte_id INT NOT NULL,
    precio_hora INT NOT NULL,
    techada BOOLEAN NOT NULL DEFAULT FALSE, --booleano obliga que sea TRUE o FALSE y por defecto es FALSE
    activa BOOLEAN NOT NULL DEFAULT TRUE,

    FOREIGN KEY (deporte_id) REFERENCES deportes(id) --FOREIGN KEY establece una relación entre la tabla canchas y deportes. Hay siempre un valor numero para un id
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE socios (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    activo BOOLEAN NOT NULL DEFAULT TRUE
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE reservas (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,

    socio_id INT NOT NULL,
    cancha_id INT NOT NULL,

    inicio DATETIME(6) NOT NULL, --YYYY-MM-DD HH:MM:SS
    fin DATETIME(6) NOT NULL,

    estado VARCHAR(20) NOT NULL DEFAULT 'confirmada',

    tarifa_hora INT NOT NULL,
    total INT NOT NULL,

    FOREIGN KEY (socio_id) REFERENCES socios(id),
    FOREIGN KEY (cancha_id) REFERENCES canchas(id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE bloqueos(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,

    cancha_id INT NOT NULL,
    fecha_bloqueo DATE NOT NULL,
    inicio DATETIME(6) NOT NULL,
    fin DATETIME(6) NOT NULL,
    motivo VARCHAR(255) NOT NULL,
    FOREIGN KEY (cancha_id) REFERENCES canchas(id)
)

-- Datos de prueba

INSERT INTO canchas (nombre, deporte_id, precio_hora, techada, activa)
VALUES
    ('Cancha de Fútbol 1', 1, 1000000, FALSE, TRUE),
    ('Cancha de Tenis 1', 2, 600000, TRUE, TRUE),
    ('Cancha de Pádel 1', 3, 800000, TRUE, TRUE);

INSERT INTO socios (nombre, email, activo)
VALUES
    ('Santiago', 'santiago@example.com', TRUE),
    ('Juan', 'juan@example.com', TRUE),
    ('Pedro', 'pedro@example.com', TRUE);