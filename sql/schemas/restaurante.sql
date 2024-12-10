DROP TABLE IF EXISTS restaurante CASCADE;
DROP TABLE IF EXISTS plato_oferta CASCADE;
DROP TABLE IF EXISTS informe_restaurante CASCADE;
DROP TABLE IF EXISTS realiza;

CREATE TABLE restaurante (
    id SERIAL PRIMARY KEY,
    restaurante VARCHAR(30) DEFAULT 'Sin nombre',
    duenio VARCHAR(30) DEFAULT 'Bad Gyal',
    distancia_reparto INTEGER DEFAULT 2,
    especialidad VARCHAR(30) DEFAULT 'Ninguna',
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
    FOREIGN KEY (id_restaurante) REFERENCES restaurante(id)
);


CREATE TABLE informe_restaurante (
    id SERIAL PRIMARY KEY,
    tiempo_preparacion_pedidos INTEGER DEFAULT 0,
    numero_ventas INTEGER DEFAULT 0,
    total_ingresado FLOAT DEFAULT 0.0
);


CREATE TABLE realiza (
    id_informe SERIAL NOT NULL, 
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    id_restaurante INTEGER NOT NULL,
    PRIMARY KEY (id_informe, fecha_inicio, fecha_fin),
    FOREIGN KEY (id_informe) REFERENCES informe_restaurante(id),
    FOREIGN KEY (id_restaurante) REFERENCES restaurante(id)
);
