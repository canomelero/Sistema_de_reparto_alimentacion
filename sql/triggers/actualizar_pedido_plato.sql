-- Implementar el trigger para cuando esté hecho Pedidos
DROP TRIGGER IF EXISTS crear_pedido_plato ON ventas_diarias;

CREATE OR REPLACE FUNCTION actualizar_pedido_plato()
RETURNS TRIGGER LANGUAGE PLPGSQL AS
$$
BEGIN
	UPDATE pedido_incluye_reparte
    SET id_plato = array_append(OLD.id_plato, NEW.id_plato)
    WHERE id_pedido = NEW.id_pedido;
    
	RETURN NEW;
END;
$$;

CREATE TRIGGER trigger_actualizar_pedido_plato
AFTER UPDATE ON ventas_diarias
FOR EACH STATEMENT
EXECUTE FUNCTION crear_pedido_plato();