-- Clave primaria id_trabajador en vez de email
CREATE TABLE trabajador (
    id_trabajador SERIAL PRIMARY KEY,
    email VARCHAR2(60) NOT NULL,
    nombre VARCHAR2(60) NOT NULL,
    direccion VARCHAR2(60) NOT NULL,
    numero_telefono VARCHAR2(20) NOT NULL
);

CREATE TABLE informe_trabajador (
    id_informe INT PRIMARY KEY,
    horas_trabajadas INT,
    numero_pedidos INT,
    salario DECIMAL(10, 2)
);

CREATE TABLE genera (
    id_informe INT NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    correo_electronico VARCHAR2(60) NOT NULL,
    PRIMARY KEY (ID_informe, Fecha_inicio),
    FOREIGN KEY (ID_informe) REFERENCES Informe_Trabajador(ID_informe),
    FOREIGN KEY (Correo_electronico) REFERENCES Trabajador(Correo_electronico)
);