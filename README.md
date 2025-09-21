# monitoring-training
Pratique des outils de monitoring pormetheus/grafana dans un contexte MLOPS

## 1. Rappel des vérification d'usage de la VM (avec OS Ubuntu)

Non demandé mais par acquis de conscience si UV n'est encore présent...

### Mise à jour globale des paquets et rattrapage éventuel des installations manquantes

```bash
# Mise à jour de la liste des paquets
sudo apt update
# Récupère et corrige d'éventuels paquets manquants
sudo apt install --fix-missing
```

### Mise à jour python3

```bash
# (Ré)installation/verif de python3 (par sureté)
sudo apt install -y python3
```

### Mise à jour pip3 et pipx

```bash
# (Ré)installation/verif de pip3 et pipx (par sureté)
sudo apt-get install -y python3-pip
sudo apt install -y pipx
pipx ensurepath
source ~/.bashrc
```

### Installation UV (gestionnaire environnement virtuel)

```bash
# Lance l’installation de uv
pipx install uv
```

### Check final des composants nécessaires (ils doivent être tous présents)

```bash
# l'ensemble des composants de base est présent
python3 --version
pip3 --version
pipx --version
uv --version
```

## 2. Prometheus

### installation

```bash
wget -c https://github.com/prometheus/prometheus/releases/download/v2.42.0/prometheus-2.42.0.linux-amd64.tar.gz
tar xvf ~/prometheus-2.42.0.linux-amd64.tar.gz
mv ~/prometheus-2.42.0.linux-amd64 ~/prometheus
rm ~/prometheus-2.42.0.linux-amd64.tar.gz
```

### Commandes scriptées

```bash
# startup
./prometheus_start.sh

# addons metrics docker daemon
./dockerd_stop.sh
./dockerd_start_metrics.sh

# addons metrics machine
./machine_monitor.sh

# addons metrics mysql
./mysql_run.sh # puis si besoin ./mysql_restart.sh
./mysql_monitor.sh
```

### Prometheus storage Write Ahead Log (WAL)

>--storage.tsbd.path [chemin du WAL]

>--storage.tsbd.retention.time [delai de retention pour le WAL]

## 3. Node Exporter

### installation

```bash
wget https://github.com/prometheus/node_exporter/releases/download/v1.0.1/node_exporter-1.0.1.linux-amd64.tar.gz
tar -xvf ~/node_exporter-1.0.1.linux-amd64.tar.gz
mv ~/node_exporter-1.0.1.linux-amd64 ~/node_exporter
rm ~/node_exporter-1.0.1.linux-amd64.tar.gz
```

## 3. Push Gateway

### installation

```bash
wget https://github.com/prometheus/pushgateway/releases/download/v1.4.1/pushgateway-1.4.1.linux-amd64.tar.gz
tar -xvf pushgateway-1.4.1.linux-amd64.tar.gz
mv pushgateway-1.4.1.linux-amd64 pushgateway
```
