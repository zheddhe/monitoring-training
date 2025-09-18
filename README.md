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