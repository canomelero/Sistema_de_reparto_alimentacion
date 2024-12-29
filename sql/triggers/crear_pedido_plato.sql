-- Implementar el trigger para cuando esté hecho Pedidos
DROP TRIGGER IF EXISTS crear_pedido_plato ON ventas_diarias;

CREATE OR REPLACE FUNCTION crear_pedido_plato()
RETURNS TRIGGER LANGUAGE PLPGSQL AS
$$
DECLARE
    v_id_pedido INT;
BEGIN
    IF (TG_OP = 'INSERT') THEN
	    INSERT INTO pedido_incluye_reparte (id_trabajador) 
        VALUES (NEW.id_trabajador)
        RETURNING id_pedido INTO v_id_pedido;

        CREATE TEMP TABLE pedido_plato (
            id_pedido INT,
            id_plato INT,
            PRIMARY KEY (id_pedido, id_plato),
            FOREIGN KEY (id_pedido) REFERENCES pedido_incluye_reparte(id_pedido),
            FOREIGN KEY (id_plato) REFERENCES plato_oferta(id_plato)
        );
    END IF;
    

    INSERT INTO 

	RETURN NEW;
END;
$$;

CREATE TRIGGER trigger_crear_pedido_plato
AFTER INSERT OR UPDATE ON ventas_diarias
FOR EACH STATEMENT
EXECUTE FUNCTION crear_pedido_plato();