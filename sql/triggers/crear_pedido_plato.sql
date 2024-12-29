-- Implementar el trigger para cuando esté hecho Pedidos
DROP TRIGGER IF EXISTS crear_pedido_plato ON ventas_diarias;

CREATE OR REPLACE FUNCTION crear_pedido_plato()
RETURNS TRIGGER LANGUAGE PLPGSQL AS
$$
BEGIN
	INSERT INTO pedido_incluye_reparte (id_plato, )
	RETURN NEW;
END;
$$;

CREATE TRIGGER trigger_crear_pedido_plato
AFTER INSERT ON ventas_diarias
FOR EACH STATEMENT
EXECUTE FUNCTION crear_pedido_plato();