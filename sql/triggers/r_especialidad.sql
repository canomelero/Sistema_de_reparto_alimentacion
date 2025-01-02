DROP TRIGGER IF EXISTS verificar_especialidad_distancia ON restaurante;

-- Lógica para manejar el RS3.3
CREATE OR REPLACE FUNCTION trigger_function()
RETURNS TRIGGER LANGUAGE PLPGSQL AS $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM restaurante
        WHERE especialidad = NEW.especialidad
          AND distancia_reparto <= 2
    ) THEN
        -- Lanzar un error si se cumple la condición
        RAISE EXCEPTION 'No puede usar la misma especialidad. Puede alejar el restaurante 
                         2km más para poder usar esa especialidad.';
    END IF;

    RETURN NEW;
END;
$$;

CREATE TRIGGER verificar_especialidad_distancia
BEFORE INSERT ON restaurante
FOR EACH ROW
EXECUTE FUNCTION trigger_function();

