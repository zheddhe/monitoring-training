docker network create my-mysql-network

# creation de la BDD (pull l'image mysql:8.0 si non présente)
docker run -d \
	--name mysql-db \
	--network my-mysql-network \
	-e MYSQL_ROOT_PASSWORD=RootPass123 \
	-e MYSQL_DATABASE=mydb \
	-e MYSQL_USER=exporter \
	-e MYSQL_PASSWORD=P455word_of_exporter \
	-p 3306:3306 mysql:8.0

# CREATE USER 'exporter'@'localhost' IDENTIFIED BY 'P455word_of_exporter' WITH MAX_USER_CONNECTIONS 3;
# GRANT PROCESS, REPLICATION CLIENT, SELECT ON *.* TO 'exporter'@'localhost';
# FLUSH PRIVILEGES;

