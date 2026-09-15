USE club_deportivo;

SHOW TABLES;

INSERT INTO reservas (
    socio_id,
    cancha_id,
    inicio,
    fin,
    estado,
    tarifa_hora,
    total
)
VALUES (
    1,
    1,
    '2026-09-15 10:00:00.000000',
    '2026-09-15 12:00:00.000000',
    'confirmada',
    1000000,
    2000000
);

SELECT
    reservas.id,
    socios.nombre AS socio,
    canchas.nombre AS cancha,
    reservas.inicio,
    reservas.fin,
    reservas.estado,
    reservas.tarifa_hora,
    reservas.total
FROM reservas
JOIN socios
    ON reservas.socio_id = socios.id
JOIN canchas
    ON reservas.cancha_id = canchas.id;


SELECT * FROM reservas;
