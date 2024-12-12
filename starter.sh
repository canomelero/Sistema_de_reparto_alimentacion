# Para ejecutar este script situarse en el directorio padre del directorio
# Sistema_de_reparto_alimentación
cd $(dirname $(find ~ -type d -name "Sistema_de_reparto_alimentacion"))
conda activate DDSI
pg_ctl -D ~/Escritorio/ddsi/pgdata -l ~/Escritorio/ddsi/logfile start
flask --app Sistema_de_reparto_alimentacion init-db
flask --app Sistema_de_reparto_alimentacion run --debug