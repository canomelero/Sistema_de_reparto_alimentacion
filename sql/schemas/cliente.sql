DROP TABLE IF EXISTS cliente CASCADE;
DROP TABLE IF EXISTS factura CASCADE;

-- Clave primaria id_cliente en vez de email
CREATE TABLE cliente (
    id_cliente SERIAL PRIMARY KEY,
    nombre VARCHAR(60),
    email VARCHAR(60),
    direccion VARCHAR(60),
    telefono VARCHAR(20)
);

CREATE TABLE factura (
    numero_pedido INT PRIMARY KEY,
    fecha DATE NOT NULL,
    id_cliente INT NOT NULL,   -- PONÍA EMAIL Y LO HE CAMBIADO A ID DEL CLIENTE
    FOREIGN KEY (numero_pedido) REFERENCES pedido_incluye_reparte(id_pedido),
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente)
);


-- Función que controla que un cliente solo podrá tener 5 pedidos facturados y 
-- en estado entregado en un mismo día

CREATE OR REPLACE FUNCTION validar_pedidos_cliente()
RETURNS TRIGGER AS $$
BEGIN
    -- Contar los pedidos del cliente facturados, con estado "entregado" y fecha actual
    IF (SELECT COUNT(*) FROM pedido_incluye_reparte ped
        JOIN factura f ON ped.id_pedido = f.numero_pedido
        WHERE f.id_cliente = NEW.id_cliente
        AND DATE(f.fecha) = CURRENT_DATE
        AND ped.estado = 'Entregado') >= 5 THEN
        RAISE EXCEPTION 'El cliente % ya tiene 3 pedidos facturados', NEW.id_cliente;
    END IF;

    -- Permitir el cambio si no se excede el límite
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


-- Creación del trigger
CREATE TRIGGER trigger_validar_pedidos
BEFORE INSERT OR UPDATE ON factura
FOR EACH ROW
EXECUTE FUNCTION validar_pedidos_cliente();


