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

### Installation

```bash
wget -c https://github.com/prometheus/prometheus/releases/download/v2.42.0/prometheus-2.42.0.linux-amd64.tar.gz
tar xvf ~/prometheus-2.42.0.linux-amd64.tar.gz
mv ~/prometheus-2.42.0.linux-amd64 ~/prometheus
rm ~/prometheus-2.42.0.linux-amd64.tar.gz
```

### Lancement

```bash
# startup (avec paramètres spéciaux ci-dessous)
### configuration YAML (inclus dans le script)
# --config.file config/prometheus.yml
### API lifecycle (inclus dans le script)
# --web.enable-lifecycle
### Storage Write Ahead Log (WAL) (non inclus dans le script bash : a ajouter si besoin)
# --storage.tsbd.path [chemin du WAL, ex: /var/lib/prometheus]
# --storage.tsbd.retention.time [delai de retention pour le WAL, ex: 30d]
./prometheus_start.sh

# rule check
./prometheus_rule_check.sh
```

## 3. Docker Daemon Exporter

### Installation et lancement

```bash
# addons metrics docker daemon
./dockerd_stop.sh
./dockerd_start_metrics.sh
```

### Désinstallation

```bash
# addons metrics docker daemon
./dockerd_stop.sh
./dockerd_start_standard.sh
```

## 4. Node Exporter

### Installation

```bash
wget https://github.com/prometheus/node_exporter/releases/download/v1.0.1/node_exporter-1.0.1.linux-amd64.tar.gz
tar -xvf ~/node_exporter-1.0.1.linux-amd64.tar.gz
mv ~/node_exporter-1.0.1.linux-amd64 ~/node_exporter
rm ~/node_exporter-1.0.1.linux-amd64.tar.gz
```

### Lancement

```bash
# addons metrics machine
./node_monitor.sh
```

## 5. MySQL Exporter

### Installation et lancement MySQL

```bash
# installation initiale
./mysql_run.sh
# relance
./mysql_restart.sh
```

### Installation et Lancement exporter

```bash
# addons metrics mysql
./mysql_monitor.sh
```

## 6. Push Gateway

### Installation

```bash
wget https://github.com/prometheus/pushgateway/releases/download/v1.4.1/pushgateway-1.4.1.linux-amd64.tar.gz
tar -xvf pushgateway-1.4.1.linux-amd64.tar.gz
mv pushgateway-1.4.1.linux-amd64 pushgateway
```

### Lancement

```bash
wget https://github.com/prometheus/pushgateway/releases/download/v1.4.1/pushgateway-1.4.1.linux-amd64.tar.gz
tar -xvf pushgateway-1.4.1.linux-amd64.tar.gz
mv pushgateway-1.4.1.linux-amd64 pushgateway
```

### Envoi de metrique directe

```bash
# ajout d'une metrique avec valeur
echo "my_metric_through_push_gateway 1" | curl -X POST --data-binary @- http://localhost:9091/metrics/job/my_fake_job/instance/my_fake_instance/my_other_label/its_value

# suppression d'un job
# curl -X DELETE http://localhost:9091/metrics/job/<job_name>
# suppression d'une instance de job
# curl -X DELETE http://localhost:9091/metrics/job/<job_name>/instance/<instance>
# suppresion d'une etiquette dans une instance de job
curl -X DELETE http://localhost:9091/metrics/job/my_fake_job/instance/my_fake_instance/my_other_label/its_value
```

## 7. Alert Manager

### Installation

```bash
wget https://github.com/prometheus/alertmanager/releases/download/v0.22.2/alertmanager-0.22.2.linux-amd64.tar.gz
tar -xvf alertmanager-0.22.2.linux-amd64.tar.gz
mv alertmanager-0.22.2.linux-amd64 alertmanager
rm alertmanager-0.22.2.linux-amd64.tar.gz
```

### Lancement

```bash
# startup
./alertmanager_start.sh

# rule check
./alertmanager_rule_check.sh
```

## 8. Kubernetes (K8s / K3s) et Helm

### Installation & lancement

```bash
# installer K3s
curl -sfL https://get.k3s.io | sh -s - --write-kubeconfig-mode 644
# verifier les versions
kubectl version
# verifier les noeuds
k3s kubectl get nodes
# installer Helm
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
# installer la stack K8s + Prometheus
kubectl config view --raw > ~/.kube/config # exportation du fichier de configuration de Kubernetes afin que Helm puisse discuter avec l'API de Kubernetes
chmod 600 ~/.kube/config
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install prometheus prometheus-community/kube-prometheus-stack --namespace monitoring  --create-namespace --set grafana.service.type=NodePort --set promotheus.service.type=NodePort
```

### Exploitation

```bash
# vérification des CR et des PODS
kubectl get crds -n monitoring  | grep monitoring
kubectl get pods -n monitoring

# passage du POD prometheus de cluster IP vers NodePort (edition via VI)
kubectl edit svc prometheus-kube-prometheus-prometheus -n monitoring
# verification du type de monitoring (pour prometheus)
kubectl get svc -n monitoring

# créer un POD (et le supprimer au préalable si besoin)
kubectl delete pod datascientest-charge-pod
kubectl apply -f config/charge-pod.yml

# vérifier des statuts et filtrer ceux en pending
kubectl get all --all-namespaces | grep -i "pending"
# afficher des infos précises sur un pod
kubectl describe pod datascientest-charge-pod

# (optionel) recuperation user et mot de passe admin grafana
kubectl --namespace monitoring get secrets prometheus-grafana -o jsonpath='{.data.admin-user}' | base64 -d ; echo
kubectl --namespace monitoring get secrets prometheus-grafana -o jsonpath="{.data.admin-password}" | base64 -d ; echo
# (optionel) forwarder le port grafana vers un port simple usuel (3000) - forwarding actif (éventuellement a mettre en background)
export POD_NAME=$(kubectl --namespace monitoring get pod -l "app.kubernetes.io/name=grafana,app.kubernetes.io/instance=prometheus" -oname)
kubectl --namespace monitoring port-forward $POD_NAME 3000
# ou bien monitorer celui utilisé par défaut
kubectl get svc -n monitoring | grep grafana
```

```bash
# exercice pratique installation de wordpress customisée via helm
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm install wordpress bitnami/wordpress --set mariadb.primary.persistence.enabled=true --set mariadb.primary.persistence.storageClass=local-path --set mariadb.primary.persistence.size=20Gi --set persistence.enabled=false --set service.type=NodePort --namespace website --create-namespace
```    

### Desinstallation

```bash
# arrêter et supprimer k3s et ses services
sudo /usr/local/bin/k3s-uninstall.sh

# supprimer helm
sudo rm -f /usr/local/bin/helm
```  