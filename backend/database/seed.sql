-- ============================================================
-- SEED: Datos de prueba — Autolavado
-- ============================================================

INSERT INTO vehiculos (placa, marca, modelo, anio, color, tipo, propietario, telefono) VALUES
('ABC-123', 'Toyota',     'Corolla',    2020, 'Blanco',  'sedan',     'Carlos Ramírez',   '3001234567'),
('DEF-456', 'Chevrolet',  'Spark',      2019, 'Rojo',    'sedan',     'María González',   '3107654321'),
('GHI-789', 'Ford',       'Explorer',   2021, 'Negro',   'camioneta', 'Juan Pérez',       '3204567890'),
('JKL-012', 'Renault',    'Duster',     2022, 'Gris',    'camioneta', 'Ana Martínez',     '3156789012'),
('MNO-345', 'Yamaha',     'FZ-S',       2023, 'Azul',    'moto',      'Luis Herrera',     '3001112233'),
('PQR-678', 'Honda',      'Civic',      2018, 'Plateado','sedan',     'Sofía Torres',     '3209988776'),
('STU-901', 'Mazda',      'CX-5',       2022, 'Rojo',    'camioneta', 'Pedro Gómez',      '3123344556'),
('VWX-234', 'Kia',        'Picanto',    2021, 'Verde',   'sedan',     'Valentina Ruiz',   '3017788990'),
('YZA-567', 'Nissan',     'Frontier',   2020, 'Negro',   'camioneta', 'Diego Morales',    '3165566778'),
('BCD-890', 'Suzuki',     'GSX-R150',   2023, 'Naranja', 'moto',      'Camila Jiménez',   '3001234000');

INSERT INTO servicios (vehiculo_id, tipo_servicio, precio, estado, observaciones) VALUES
(1,  'lavado_basico',    15000, 'completado',  'Cliente frecuente'),
(1,  'encerado',         35000, 'completado',  'Cera especial para color blanco'),
(2,  'lavado_completo',  25000, 'completado',  NULL),
(3,  'lavado_premium',   45000, 'en_proceso',  'Camioneta con barro en ruedas'),
(3,  'tapizado',         60000, 'pendiente',   'Tapizado completo de 5 puestos'),
(4,  'lavado_basico',    15000, 'completado',  NULL),
(5,  'lavado_basico',    10000, 'completado',  'Tarifa especial para motos'),
(6,  'lavado_completo',  25000, 'pendiente',   'Agendar para las 3pm'),
(7,  'motor',            55000, 'en_proceso',  'Limpieza de motor con vapor'),
(8,  'lavado_premium',   45000, 'completado',  NULL),
(9,  'lavado_completo',  25000, 'pendiente',   'Requiere secado especial'),
(10, 'lavado_basico',    10000, 'completado',  'Moto deportiva');
