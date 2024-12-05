-- Clave primaria id_trabajador en vez de email
CREATE TABLE trabajador (
    id_trabajador SERIAL PRIMARY KEY,
    email VARCHAR2(60),
    nombre VARCHAR2(60),
    direccion VARCHAR2(60),
    numero_telefono VARCHAR2(20)
);

CREATE TABLE informe_trabajador (
    id_informe INT PRIMARY KEY,
    horas_trabajadas INT DEFAULT 0,
    numero_pedidos INT DEFAULT 0,
    salario INT
);

CREATE TABLE genera (
    id_informe INT NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    email VARCHAR2(60) NOT NULL,
    PRIMARY KEY (id_informe, fecha_inicio),
    FOREIGN KEY (id_informe) REFERENCES informe_trabajador(id_informe),
    FOREIGN KEY (email) REFERENCES trabajador(email)
);