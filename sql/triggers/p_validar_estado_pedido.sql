DROP TRIGGER IF EXISTS trg_validar_modificacion_pedido ON pedido_incluye_reparte;

-- Crear la función para validar la modificación
CREATE OR REPLACE FUNCTION validar_estado_pedido()
RETURNS TRIGGER AS $$
BEGIN
    -- Validar si el estado actual del pedido es 'En reparto' o 'Entregado'
    IF OLD.estado IN ('En reparto', 'Entregado') THEN
        RAISE EXCEPTION 'No es posible modificar un pedido que está en estado En Camino o Entregado';
    END IF;
    -- Permitir la operación si no aplica la restricción
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Crear el trigger que utiliza la función
CREATE TRIGGER trg_validar_modificacion_pedido
BEFORE UPDATE ON pedido_incluye_reparte
FOR EACH ROW
EXECUTE FUNCTION validar_estado_pedido();