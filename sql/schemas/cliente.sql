DROP TABLE IF EXISTS cliente CASCADE;

CREATE TABLE cliente (
    id SERIAL PRIMARY KEY,
    nombre TEXT UNIQUE NOT NULL,
    email TEXT NOT NULL,
    direccion TEXT NOT NULL,
    telefono TEXT NOT NULL
);