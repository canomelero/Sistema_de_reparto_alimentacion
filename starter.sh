# Para ejecutar este script situarse en el directorio padre del directorio
# Sistema_de_reparto_alimentación
conda activate DDSI
pg_ctl -D ./Sistema_de_reparto_alimentacion/pgdata -l Sistema_de_reparto_alimentacion/logfile start
flask --app Sistema_de_reparto_alimentacion init-db
flask --app Sistema_de_reparto_alimentacion run --debug