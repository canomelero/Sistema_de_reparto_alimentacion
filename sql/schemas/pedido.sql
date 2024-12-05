-- Tabla: Pedido-Incluye-Reparte
CREATE TABLE pedido_incluye_reparte (
    mumero_pedido INT PRIMARY KEY,
    id_plato INT NOT NULL,
    email VARCHAR2(30) NOT NULL,
    direccion_entrega VARCHAR(60),
    observaciones VARCHAR(60),
    precio FLOAT,
    estado VARCHAR2(20),
    tiempo_preparacion INT DEFAULT 20,
    tiempo_entrega INT DEFAULT 5,
    FOREIGN KEY (id_plato) REFERENCES plato_oferta(id_plato),
    FOREIGN KEY (email) REFERENCES cliente(email)
);
