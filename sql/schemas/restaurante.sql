-- Tabla: Restaurante
CREATE TABLE Restaurante (
    ID_restaurante INT PRIMARY KEY,
    Nombre_restaurante VARCHAR2(100) NOT NULL,
    Nombre_dueño VARCHAR2(100),
    Distancia_reparto DECIMAL(5, 2),
    Especialidad VARCHAR2(100),
    Horario VARCHAR2(50)
);

-- Tabla: Plato-Oferta
CREATE TABLE Plato_Oferta (
    ID_plato INT PRIMARY KEY,
    ID_restaurante INT NOT NULL,
    Nombre VARCHAR2(100) NOT NULL,
    Ingredientes TEXT,
    Descripcion TEXT,
    Tiempo_preparacion INT,
    Precio DECIMAL(10, 2),
    Disponibilidad BOOLEAN,
    FOREIGN KEY (ID_restaurante) REFERENCES Restaurante(ID_restaurante)
);

-- Tabla: Factura
CREATE TABLE Factura (
    Fecha DATE NOT NULL,
    Numero_pedido INT NOT NULL,
    Correo_electronico VARCHAR2(100) NOT NULL,
    PRIMARY KEY (Fecha, Numero_pedido),
    FOREIGN KEY (Numero_pedido) REFERENCES Pedido_Incluye_Reparte(Numero_pedido),
    FOREIGN KEY (Correo_electronico) REFERENCES Cliente(Correo_electronico)
);

-- Tabla: Informe Restaurante
CREATE TABLE Informe_Restaurante (
    ID_informe INT PRIMARY KEY,
    Tiempo_preparacion_pedidos INT,
    Numero_ventas INT,
    Total_ingresado DECIMAL(15, 2)
);