DROP TRIGGER IF EXISTS validar_pedidos_cliente ON factura;

-- Lógica para manejar el RS2.4
CREATE OR REPLACE FUNCTION validar_pedidos_cliente()
RETURNS TRIGGER AS $$
BEGIN
    -- Contar los pedidos del cliente facturados, con estado "entregado" y fecha actual
    IF (SELECT COUNT(*) FROM pedido_incluye_reparte ped
        JOIN factura f ON ped.id_pedido = f.numero_pedido
        WHERE f.id_cliente = NEW.id_cliente
        AND DATE(f.fecha) = CURRENT_DATE
        AND ped.estado = 'Entregado') >= 5 THEN
        RAISE EXCEPTION 'El cliente % ya tiene 5 pedidos facturados', NEW.id_cliente;
    END IF;

    -- Permitir el cambio si no se excede el límite
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


-- Crear el trigger asociado
CREATE TRIGGER trigger_validar_pedidos
BEFORE INSERT ON factura
FOR EACH ROW
EXECUTE FUNCTION validar_pedidos_cliente();