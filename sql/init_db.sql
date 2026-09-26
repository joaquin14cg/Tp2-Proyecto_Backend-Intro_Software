-- ============================================================
-- BASE DE DATOS
-- ============================================================

CREATE DATABASE IF NOT EXISTS club_deportivo
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE club_deportivo;


-- ============================================================
-- USUARIO DE LA APLICACIÓN
-- ============================================================

CREATE USER IF NOT EXISTS 'club_admin'@'localhost'
    IDENTIFIED BY 'lanzillotta';

GRANT ALL PRIVILEGES ON club_deportivo.*
    TO 'club_admin'@'localhost';

FLUSH PRIVILEGES;


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
);

INSERT INTO deportes (nombre) VALUES
    ('Fútbol'),
    ('Tenis'),
    ('Pádel');


-- ============================================================
-- CANCHAS
-- ============================================================

CREATE TABLE canchas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    deporte_id INT NOT NULL,
    precio_hora DECIMAL(10,2) NOT NULL,
    techada BOOLEAN NOT NULL DEFAULT FALSE,
    activa BOOLEAN NOT NULL DEFAULT TRUE,

    CONSTRAINT fk_cancha_deporte
        FOREIGN KEY (deporte_id)
        REFERENCES deportes(id)
);


INSERT INTO canchas
    (nombre, deporte_id, precio_hora, techada, activa)
VALUES
    ('Cancha Fútbol 1', 1, 15000.00, TRUE, TRUE),
    ('Cancha Fútbol 2', 1, 13000.00, FALSE, TRUE),
    ('Cancha Tenis 1', 2, 9000.00, FALSE, TRUE),
    ('Cancha Pádel 1', 3, 10000.00, TRUE, TRUE),
    ('Cancha Pádel 2', 3, 10000.00, FALSE, TRUE);


-- ============================================================
-- SOCIOS
-- ============================================================

CREATE TABLE socios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE
);


INSERT INTO socios
    (nombre, email)
VALUES
    ('Juan Pérez', 'juan.perez@gmail.com'),
    ('María González', 'maria.gonzalez@gmail.com'),
    ('Pedro Rodríguez', 'pedro.rodriguez@gmail.com'),
    ('Lucía Fernández', 'lucia.fernandez@gmail.com'),
    ('Nicolás López', 'nicolas.lopez@gmail.com');


-- ============================================================
-- RESERVAS
-- ============================================================

CREATE TABLE reservas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    socio_id INT NOT NULL,
    cancha_id INT NOT NULL,
    inicio DATETIME NOT NULL,
    fin DATETIME NOT NULL,
    estado VARCHAR(50) NOT NULL,
    tarifa_hora DECIMAL(10,2) NOT NULL,
    total DECIMAL(10,2) NOT NULL,

    CONSTRAINT fk_reserva_socio
        FOREIGN KEY (socio_id)
        REFERENCES socios(id),

    CONSTRAINT fk_reserva_cancha
        FOREIGN KEY (cancha_id)
        REFERENCES canchas(id)
);


INSERT INTO reservas
    (socio_id, cancha_id, inicio, fin, estado, tarifa_hora, total)
VALUES
    (
        1,
        1,
        '2026-10-15 18:00:00',
        '2026-10-15 20:00:00',
        'CONFIRMADA',
        15000.00,
        30000.00
    ),
    (
        2,
        3,
        '2026-10-16 17:00:00',
        '2026-10-16 18:00:00',
        'CONFIRMADA',
        9000.00,
        9000.00
    ),
    (
        3,
        4,
        '2026-10-17 19:00:00',
        '2026-10-17 20:00:00',
        'CONFIRMADA',
        10000.00,
        10000.00
    );


-- ============================================================
-- BLOQUEOS
-- ============================================================

CREATE TABLE bloqueos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cancha_id INT NOT NULL,
    fecha_bloqueo DATE NOT NULL,
    inicio TIME NOT NULL,
    fin TIME NOT NULL,
    motivo VARCHAR(255),

    CONSTRAINT fk_bloqueo_cancha
        FOREIGN KEY (cancha_id)
        REFERENCES canchas(id)
);


INSERT INTO bloqueos
    (cancha_id, fecha_bloqueo, inicio, fin, motivo)
VALUES
    (
        1,
        '2026-10-15',
        '16:00:00',
        '18:00:00',
        'Mantenimiento'
    ),
    (
        3,
        '2026-10-16',
        '15:00:00',
        '17:00:00',
        'Limpieza'
    );


-- ============================================================
-- FINAL
-- ============================================================

SELECT 'Base de datos inicializada correctamente.' AS mensaje;