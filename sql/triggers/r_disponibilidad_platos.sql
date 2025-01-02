DROP TRIGGER IF EXISTS actualizar_disponibilidad ON plato_oferta;

-- Lógica para manejar el RS3.2
CREATE OR REPLACE FUNCTION actualizar_disponibilidad()
RETURNS TRIGGER LANGUAGE PLPGSQL AS $$
DECLARE 
    nombre_plato VARCHAR(30);
BEGIN
    IF NEW.cantidad = 0 THEN
        UPDATE plato_oferta
        SET disponibilidad = false
        WHERE id_plato = NEW.id_plato; 

        SELECT nombre INTO nombre_plato FROM plato_oferta WHERE id_plato = NEW.id_plato;

        RAISE EXCEPTION 'El plato ''%'' no está disponible', nombre_plato;
    ELSEIF NEW.cantidad > 5 AND OLD.disponibilidad = false THEN
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
