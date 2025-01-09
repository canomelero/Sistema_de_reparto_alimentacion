-- Insertar dos restaurantes
INSERT INTO restaurante (nombre, duenio, distancia_reparto, especialidad, 
horario_apertura, horario_cierre) VALUES 
('La Pizzería', 'Juan Pérez', 3, 'Pizza', '12:00:00', '23:00:00'),
('El Sabor Mexicano', 'María García', 5, 'Tacos', '10:00:00', '22:00:00');

-- Insertar platos para el restaurante 'La Pizzería'
INSERT INTO plato_oferta (id_restaurante, nombre, ingredientes, tiempo_preparacion, precio,
disponibilidad, cantidad) VALUES
(1, 'Pizza Margarita', 'Tomate, queso mozzarella, albahaca', 15, 8.5, true, 6),
(1, 'Pizza Pepperoni', 'Tomate, queso mozzarella, pepperoni', 18, 9.5, true, 6),
(2, 'Tacos al Pastor', 'Cerdo, piña, cilantro, cebolla', 10, 6.5, true, 6),
(2, 'Tacos de Carne Asada', 'Carne asada, cebolla, cilantro, salsa', 12, 7.5, true, 6);

-- Insertar dos clientes
INSERT INTO cliente (nombre, email, direccion, telefono) VALUES
('Carlos Rodríguez', 'carlos@example.com', 'Calle Falsa 123', '123456789'),
('Ana Gómez', 'ana@example.com', 'Avenida Real 456', '987654321');


INSERT INTO trabajador (email, nombre, direccion, numero_telefono, disponibilidad)
VALUES 
('juan.perez@ejemplo.com', 'Juan Pérez', 'Calle Ficticia 123', '1234567890', true),
('ana.lopez@ejemplo.com', 'Ana López', 'Avenida Principal 456', '0987654321', true),
('maria.gomez@ejemplo.com', 'María Gómez', 'Calle Secundaria 789', '1122334455', true),
('carlos.ruiz@ejemplo.com', 'Carlos Ruiz', 'Avenida Las Flores 321', '2233445566', true);