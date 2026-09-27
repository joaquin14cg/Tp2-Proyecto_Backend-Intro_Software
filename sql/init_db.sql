SET NAMES utf8mb4; -- sirve para trabajar con caracteres con tildes
 
CREATE DATABASE IF NOT EXISTS club_deportivo
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE club_deportivo;

-- ============================================================
-- LIMPIAR TABLAS
-- ============================================================

DROP TABLE IF EXISTS bloqueos;
DROP TABLE IF EXISTS reservas;
DROP TABLE IF EXISTS socios;
DROP TABLE IF EXISTS canchas;
DROP TABLE IF EXISTS deportes;


-- ============================================================
-- DEPORTES
-- ============================================================

CREATE TABLE deportes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

INSERT INTO deportes (nombre) VALUES
    ('Fútbol'),
    ('Tenis'),
    ('Pádel');


-- ============================================================
-- CANCHAS
-- ============================================================

CREATE TABLE canchas (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    id_deporte INT NOT NULL,
    precio_hora INT NOT NULL,
    techada BOOLEAN NOT NULL DEFAULT FALSE,
    activa BOOLEAN NOT NULL DEFAULT TRUE,

    FOREIGN KEY (id_deporte)
        REFERENCES deportes(id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;


INSERT INTO canchas
    (nombre, id_deporte, precio_hora, techada, activa)
VALUES
    ('Cancha Fútbol 1', 1, 15000, TRUE, TRUE),
    ('Cancha Fútbol 2', 1, 13000, FALSE, TRUE),
    ('Cancha Tenis 1', 2, 9000, FALSE, TRUE),
    ('Cancha Pádel 1', 3, 10000, TRUE, TRUE),
    ('Cancha Pádel 2', 3, 10000, FALSE, TRUE);


-- ============================================================
-- SOCIOS
-- ============================================================

CREATE TABLE socios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(150) NOT NULL UNIQUE,
    activo BOOLEAN NOT NULL DEFAULT TRUE
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;




INSERT INTO socios
    (nombre, email, activo)
VALUES
    ('Juan Pérez', 'juan.perez@gmail.com', TRUE),
    ('María González', 'maria.gonzalez@gmail.com', TRUE),
    ('Pedro Rodríguez', 'pedro.rodriguez@gmail.com', TRUE),
    ('Lucía Fernández', 'lucia.fernandez@gmail.com', TRUE),
    ('Nicolás López', 'nicolas.lopez@gmail.com', TRUE);


-- ============================================================
-- RESERVAS
-- ============================================================

CREATE TABLE reservas (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,

    socio_id INT NOT NULL,
    cancha_id INT NOT NULL,

    inicio DATETIME(6) NOT NULL,
    fin DATETIME(6) NOT NULL,

    estado VARCHAR(20) NOT NULL DEFAULT 'confirmada',

    tarifa_hora INT NOT NULL,
    total INT NOT NULL,

    FOREIGN KEY (socio_id)
        REFERENCES socios(id),

    FOREIGN KEY (cancha_id)
        REFERENCES canchas(id)
);

INSERT INTO reservas
    (socio_id, cancha_id, inicio, fin, estado, tarifa_hora, total)
VALUES
(
    1,
    1,
    '2026-10-15 10:00:00.000000',
    '2026-10-15 12:00:00.000000',
    'confirmada',
    15000,
    30000
),
(
    2,
    3,
    '2026-10-16 15:00:00.000000',
    '2026-10-16 16:00:00.000000',
    'confirmada',
    9000,
    9000
);


-- ============================================================
-- BLOQUEOS
-- ============================================================

CREATE TABLE bloqueos (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,

    cancha_id INT NOT NULL,
    fecha_bloqueo DATE NOT NULL,
    inicio DATETIME(6) NOT NULL,
    fin DATETIME(6) NOT NULL,
    motivo VARCHAR(255) NOT NULL,

    FOREIGN KEY (cancha_id)
        REFERENCES canchas(id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;


INSERT INTO bloqueos
    (cancha_id, fecha_bloqueo, inicio, fin, motivo)
VALUES
(
    1,
    '2026-10-15',
    '2026-10-15 16:00:00.000000',
    '2026-10-15 18:00:00.000000',
    'Mantenimiento'
),
(3,  '2026-10-16', '2026-10-16 12:00:00.000000',   '2026-10-16 14:00:00.000000',
    'Limpieza'
);

-- ============================================================
-- FINAL
-- ============================================================

SELECT 'Base de datos inicializada correctamente.' AS mensaje;