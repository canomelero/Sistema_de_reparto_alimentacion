DROP TABLE IF EXISTS trabajador CASCADE;
DROP TABLE IF EXISTS informe_trabajador CASCADE;
DROP TABLE IF EXISTS genera CASCADE;

CREATE TABLE trabajador (
    id_trabajador SERIAL PRIMARY KEY,
    email VARCHAR(60),
    nombre VARCHAR(60),
    direccion VARCHAR(60),
    numero_telefono VARCHAR(20),
    disponibilidad BOOLEAN DEFAULT true
);

CREATE TABLE informe_trabajador (
    id_informe SERIAL PRIMARY KEY,
    minutos_trabajados INT DEFAULT 0,
    numero_pedidos INT DEFAULT 0,
    salario INT
);

CREATE TABLE genera (
    id_informe INT NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    id_trabajador INT NOT NULL,
    PRIMARY KEY (id_informe, fecha_inicio),
    FOREIGN KEY (id_informe) REFERENCES informe_trabajador(id_informe),
    FOREIGN KEY (id_trabajador) REFERENCES trabajador(id_trabajador)
);