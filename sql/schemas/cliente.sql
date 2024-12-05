DROP TABLE IF EXISTS cliente CASCADE;

-- Clave primaria id_cliente en vez de email
CREATE TABLE cliente (
    id_cliente SERIAL PRIMARY KEY,
    nombre VARCHAR(60),
    email VARCHAR(60),
    direccion VARCHAR(60),
    telefono VARCHAR(20)
);

-- CREATE TABLE Factura (
--     fecha DATE NOT NULL,
--     numero_pedido INT NOT NULL,
--     email TEXT NOT NULL,
--     PRIMARY KEY (fecha, numero_pedido),
--     FOREIGN KEY (numero_pedido) REFERENCES pedido_incluye_reparte(numero_pedido),
--     FOREIGN KEY (correo_electronico) REFERENCES cliente(correo_electronico)
-- );

