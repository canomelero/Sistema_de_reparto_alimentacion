DROP TABLE IF EXISTS cliente CASCADE;

-- Clave primaria id_cliente en vez de email
CREATE TABLE cliente (
    id_cliente SERIAL PRIMARY KEY,
    nombre TEXT UNIQUE NOT NULL,
    email TEXT NOT NULL,
    direccion TEXT NOT NULL,
    telefono TEXT NOT NULL
);

-- CREATE TABLE Factura (
--     fecha DATE NOT NULL,
--     numero_pedido INT NOT NULL,
--     email TEXT NOT NULL,
--     PRIMARY KEY (Fecha, Numero_pedido),
--     FOREIGN KEY (Numero_pedido) REFERENCES Pedido_Incluye_Reparte(Numero_pedido),
--     FOREIGN KEY (Correo_electronico) REFERENCES Cliente(Correo_electronico)
-- );

