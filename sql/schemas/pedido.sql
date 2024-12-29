DROP TABLE IF EXISTS pedido_incluye_reparte CASCADE;
DROP TABLE IF EXISTS pedido_plato CASCADE;

CREATE TABLE pedido_incluye_reparte (
    id_pedido SERIAL PRIMARY KEY,
    id_trabajador INT NOT NULL,
    direccion_entrega VARCHAR(60),
    observaciones VARCHAR(60),
    precio FLOAT,
    estado VARCHAR(20),
    tiempo_preparacion INT DEFAULT 20,
    tiempo_entrega INT DEFAULT 5,
    FOREIGN KEY (id_trabajador) REFERENCES trabajador(id_trabajador)
);

-- Esta tabla debe de ser temporal, creada de forma normal para hacer pruebas, ya lo cambiaré.
CREATE TABLE pedido_plato (
    id_pedido INT,
    id_plato INT
)