DROP TRIGGER IF EXISTS trg_cambiar_disponibilidad ON pedido_incluye_reparte;

-- Crear la función para validar la modificación
CREATE OR REPLACE FUNCTION cambiar_disponibilidad()
RETURNS TRIGGER AS $$
BEGIN
    -- Validar si el estado actual del pedido es 'En reparto' o 'Entregado'
    IF NEW.estado IN ('Entregado') THEN
        UPDATE trabajador 
        SET disponibilidad = True WHERE id_trabajador IN (SELECT id_trabajador 
        FROM pedido_incluye_reparte WHERE id_pedido = NEW.id_pedido);
    END IF;
    -- Permitir la operación si no aplica la restricción
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Crear el trigger que utiliza la función
CREATE TRIGGER trg_cambiar_disponibilidad
AFTER UPDATE ON pedido_incluye_reparte
FOR EACH ROW
EXECUTE FUNCTION cambiar_disponibilidad();