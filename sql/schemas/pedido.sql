-- Tabla: Pedido-Incluye-Reparte
CREATE TABLE Pedido_Incluye_Reparte (
    Numero_pedido INT PRIMARY KEY,
    ID_plato INT NOT NULL,
    Correo_electronico VARCHAR2(100) NOT NULL,
    Direccion_entrega TEXT,
    Observaciones TEXT,
    Precio FLOAT,
    Estado VARCHAR2(50),
    Tiempo_preparacion INT,
    Tiempo_entrega INT,
    FOREIGN KEY (ID_plato) REFERENCES Plato_Oferta(ID_plato),
    FOREIGN KEY (Correo_electronico) REFERENCES Cliente(Correo_electronico)
);
