-- Tabla: Cliente
CREATE TABLE Cliente (
    Correo_electronico VARCHAR2(100) PRIMARY KEY,
    Nombre_completo VARCHAR2(100) NOT NULL,
    Telefono VARCHAR2(15),
    Direccion TEXT
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
