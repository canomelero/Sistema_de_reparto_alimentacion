CREATE TABLE restaurante (
    id SERIAL PRIMARY KEY,
    nombre_restaurante VARCHAR(30),
    nombre_dueño VARCHAR(30),
    distancia_reparto INTEGER DEFAULT 2,
    especialidad VARCHAR(30),
    horario_apertura TIME DEFAULT '9:00',
    horario_cierre TIME DEFAULT '21:00'
);


CREATE TABLE plato_oferta (
    id_plato SERIAL PRIMARY KEY,
    id_restaurante INTEGER NOT NULL,
    nombre VARCHAR(30) NOT NULL,
    ingredientes VARCHAR(60),
    tiempo_preparacion INTEGER DEFAULT 10,
    precio FLOAT NOT NULL,
    disponibilidad BOOLEAN DEFAULT true,
    FOREIGN KEY (id_restaurante) REFERENCES restaurante(id_restaurante)
);

CREATE TABLE realiza (
    id_informe SERIAL NOT NULL, 
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    id_restaurante NOT NULL,
    PRIMARY KEY (id_informe, fecha_inicio, fecha_fin),
    FOREIGN KEY (id_informe) REFERENCES informe_restaurante(id_informe),
    FOREIGN KEY (id_restaurante) REFERENCES restaurante(id_restaurante)
)


CREATE TABLE informe_restaurante (
    id_informe SERIAL PRIMARY KEY,
    tiempo_preparacion_pedidos INTEGER DEFAULT 0,
    numero_ventas INTEGER DEFAULT 0,
    total_ingresado FLOAT DEFAULT 0.0
);