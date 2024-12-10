DROP TABLE IF EXISTS pedido_incluye_reparte CASCADE;

CREATE TABLE pedido_incluye_reparte (
    mumero_pedido INT PRIMARY KEY,
    id_plato INT NOT NULL,
    id_trabajador INT NOT NULL,
    direccion_entrega VARCHAR(60),
    observaciones VARCHAR(60),
    precio FLOAT,
    estado VARCHAR(20),
    tiempo_preparacion INT DEFAULT 20,
    tiempo_entrega INT DEFAULT 5,
    FOREIGN KEY (id_plato) REFERENCES plato_oferta(id_plato),
    FOREIGN KEY (id_trabajador) REFERENCES trabajador(id_trabajador)
);
