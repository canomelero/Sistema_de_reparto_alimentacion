DROP TABLE IF EXISTS restaurante CASCADE;
DROP TABLE IF EXISTS plato_oferta CASCADE;
DROP TABLE IF EXISTS informe_restaurante CASCADE;
DROP TABLE IF EXISTS ventas_diarias CASCADE;

-- Los valores por defectos están gestionados con el post directamente
CREATE TABLE restaurante (
    id SERIAL PRIMARY KEY,
    restaurante VARCHAR(30),
    duenio VARCHAR(30),
    distancia_reparto INTEGER DEFAULT 2,
    especialidad VARCHAR(30),
    horario_apertura TIME,
    horario_cierre TIME
);


CREATE TABLE plato_oferta (
    id_plato SERIAL PRIMARY KEY,
    id_restaurante INTEGER NOT NULL,
    nombre VARCHAR(30) NOT NULL,
    ingredientes VARCHAR(60),
    tiempo_preparacion INTEGER,
    precio FLOAT NOT NULL,
    disponibilidad BOOLEAN,
    FOREIGN KEY (id_restaurante) REFERENCES restaurante(id)
);


CREATE TABLE informe_restaurante (
    id_informe SERIAL PRIMARY KEY,
    id_restaurante INTEGER NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    tiempo_preparacion_pedidos INTEGER DEFAULT 0,
    numero_ventas INTEGER DEFAULT 0,
    total_ingresado FLOAT DEFAULT 0.0,
    FOREIGN KEY (id_restaurante) REFERENCES restaurante(id)
);


CREATE TABLE ventas_diarias (
    id SERIAL PRIMARY KEY,
    id_restaurante INTEGER NOT NULL,
    fecha DATE NOT NULL,
    tiempo_preparacion INTEGER,
    total_ingresado FLOAT,
    platos_vendidos INTEGER DEFAULT 0,
    FOREIGN KEY (id_restaurante) REFERENCES restaurante(id)
);