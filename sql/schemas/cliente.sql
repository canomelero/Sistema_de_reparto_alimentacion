DROP TABLE IF EXISTS cliente CASCADE;
DROP TABLE IF EXISTS factura CASCADE;

-- Clave primaria id_cliente en vez de email
CREATE TABLE cliente (
    id_cliente SERIAL PRIMARY KEY,
    nombre VARCHAR(60),
    email VARCHAR(60),
    direccion VARCHAR(60),
    telefono VARCHAR(20)
);

CREATE TABLE factura (
    numero_pedido INT PRIMARY KEY,
    fecha DATE NOT NULL,
    id_cliente INT NOT NULL,   -- PONÍA EMAIL Y LO HE CAMBIADO A ID DEL CLIENTE
    FOREIGN KEY (numero_pedido) REFERENCES pedido_incluye_reparte(numero_pedido),
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente)
);



