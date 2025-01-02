DROP TRIGGER IF EXISTS actualizar_disponibilidad ON plato_oferta;

-- Lógica para manejar el RS3.2
CREATE OR REPLACE FUNCTION actualizar_disponibilidad()
RETURNS TRIGGER LANGUAGE PLPGSQL AS $$
BEGIN
    IF NEW.cantidad = 0 AND OLD.disponibilidad IS DISTINCT FROM false THEN
        UPDATE plato_oferta
        SET disponibilidad = false
        WHERE id_plato = NEW.id_plato; 
    ELSEIF NEW.cantidad > 5 AND OLD.disponibilidad IS DISTINCT FROM true THEN
        UPDATE plato_oferta
        SET disponibilidad = true
        WHERE id_plato = NEW.id_plato;
    END IF;

    RETURN NEW;
END;
$$;

-- Crear el trigger asociado
CREATE TRIGGER trigger_actualizar_disponibilidad
AFTER UPDATE ON plato_oferta
FOR EACH ROW
EXECUTE FUNCTION actualizar_disponibilidad();
