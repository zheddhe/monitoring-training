# creation de l'exporter (pull l'image prom/mysqld-exporter si non présente)
# docker run \
# 	-p 9104:9104 \
# 	--network my-mysql-network \
# 	-e DATA_SOURCE_NAME="exporter:P455word_of_exporter@(mysql-db:3306)/" \
# 	prom/mysqld-exporter

# utilisation plutôt d'un fichier de configuration my.cnf local à binder vers l'instance docker mysql-exporter pour passer le DATA_SOURCE_NAME
docker run -d \
	-p 9104:9104 \
	--network my-mysql-network \
	-v $(pwd)/my.cnf:/my.cnf:ro \
	prom/mysqld-exporter \
	--config.my-cnf=/my.cnf
