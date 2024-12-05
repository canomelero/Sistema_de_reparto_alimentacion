DROP TABLE IF EXISTS cliente CASCADE;

CREATE TABLE cliente (
    id SERIAL PRIMARY KEY,
    nombre TEXT UNIQUE NOT NULL,
    email TEXT NOT NULL,
    direccion TEXT NOT NULL,
    telefono TEXT NOT NULL
);

-- CREATE TABLE Factura (
--     Fecha DATE NOT NULL,
--     Numero_pedido INT NOT NULL,
--     Correo_electronico VARCHAR2(100) NOT NULL,
--     PRIMARY KEY (Fecha, Numero_pedido),
--     FOREIGN KEY (Numero_pedido) REFERENCES Pedido_Incluye_Reparte(Numero_pedido),
--     FOREIGN KEY (Correo_electronico) REFERENCES Cliente(Correo_electronico)
-- );

