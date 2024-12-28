# Para ejecutar este script situarse en el directorio padre del directorio
# Sistema_de_reparto_alimentación.
# Luego poner: . starter.sh
# El . de antes se hace para que te lo ejecute en la terminal actual y no en una en segundo plano

cd $(dirname $(find ~ -type d -name "Sistema_de_reparto_alimentacion"))
condaInit
conda activate DDSI
# Copiar y pegar y modificar cada uno el suyo de pg_ctl
pg_ctl -D ~/Desktop/DDSI/Sistema_de_reparto_alimentacion/pgdata \ 
-l ~/Desktop/DDSI/Sistema_de_reparto_alimentacion/logfile start


flask --app Sistema_de_reparto_alimentacion init-db
flask --app Sistema_de_reparto_alimentacion run --debug