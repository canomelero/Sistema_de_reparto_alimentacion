-- Tabla: Trabajador
CREATE TABLE Trabajador (
    Correo_electronico VARCHAR2(60) PRIMARY KEY,
    Nombre VARCHAR2(60) NOT NULL,
    Direccion VARCHAR2(60),
    Numero_telefono VARCHAR2(20)
);

-- Tabla: Informe Trabajador
CREATE TABLE Informe_Trabajador (
    ID_informe INT PRIMARY KEY,
    Horas_trabajadas INT,
    Numero_pedidos INT,
    Salario DECIMAL(10, 2)
);

-- Tabla: Genera
CREATE TABLE Genera (
    ID_informe INT NOT NULL,
    Fecha_inicio DATE NOT NULL,
    Fecha_fin DATE NOT NULL,
    Correo_electronico VARCHAR2(60) NOT NULL,
    PRIMARY KEY (ID_informe, Fecha_inicio),
    FOREIGN KEY (ID_informe) REFERENCES Informe_Trabajador(ID_informe),
    FOREIGN KEY (Correo_electronico) REFERENCES Trabajador(Correo_electronico)
);