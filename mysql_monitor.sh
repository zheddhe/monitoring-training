# creation de l'exporter (pull l'image prom/mysqld-exporter si non présente)
# utilisation d'un fichier de configuration my.cnf local à binder vers l'instance docker mysql-exporter pour passer le DATA_SOURCE_NAME
docker run -d \
	-p 9104:9104 \
	--network my-mysql-network \
	-v $(pwd)/my.cnf:/my.cnf:ro \
	prom/mysqld-exporter \
	--config.my-cnf=/my.cnf
