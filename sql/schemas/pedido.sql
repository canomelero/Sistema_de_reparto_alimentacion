DROP TABLE IF EXISTS pedido_incluye_reparte CASCADE;
DROP TABLE IF EXISTS pedido_plato CASCADE;

CREATE TABLE pedido_incluye_reparte (
    id_pedido SERIAL PRIMARY KEY,
    id_trabajador INT NOT NULL,
    direccion_entrega VARCHAR(60),
    observaciones VARCHAR(60),
    precio FLOAT,
    estado VARCHAR(20),
    tiempo_preparacion INT,
    tiempo_entrega INT,
    FOREIGN KEY (id_trabajador) REFERENCES trabajador(id_trabajador)
);

CREATE TABLE pedido_plato (
    id_pedido INT,
    id_plato INT,
    FOREIGN KEY (id_pedido) REFERENCES pedido_incluye_reparte(id_pedido),
    FOREIGN KEY (id_plato) REFERENCES plato_oferta(id_plato)
)