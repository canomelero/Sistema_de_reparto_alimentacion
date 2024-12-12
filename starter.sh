# Para ejecutar este script situarse en el directorio padre del directorio
# Sistema_de_reparto_alimentación
cd $(dirname $(find ~ -type d -name "Sistema_de_reparto_alimentacion"))
conda activate DDSI
pg_ctl -D ./Sistema_de_reparto_alimentacion/pgdata -l Sistema_de_reparto_alimentacion/logfile start
flask --app Sistema_de_reparto_alimentacion init-db
flask --app Sistema_de_reparto_alimentacion run --debug