# requêtes d'illustration
```python
prometheus_http_requests_total
prometheus_http_requests_total{handler="/graph"}
prometheus_http_requests_total{code=~"20."}
prometheus_http_requests_total{code=~"20."} offset 10m
prometheus_http_requests_total{code="200", handler="/graph"} [5m]
prometheus_http_requests_total{code="200"} + prometheus_http_requests_total{code="200", handler=~"/api/.*"}
sum(prometheus_http_requests_total)
sum by (handler) (prometheus_http_requests_total)
avg_over_time(prometheus_http_requests_total [5m])
max by (handler) (prometheus_http_requests_total) [20m:1m]
avg_over_time(max by (handler) (prometheus_http_requests_total) [20m:1m] )
```

# requêtes pour pods kubernetes
```python
# Trouver le nombre de pods par Namespace
sum by (namespace) (kube_pod_info)
# Rechercher les surcharge processeur prévisible (ressources demandées par tous les PODS Kubernetes Vs ressources disponibles sur le node)
# valeur négative OK, valeur positive : surcharge détectée
sum(kube_pod_container_resource_limits{resource="cpu"}) - sum(kube_node_status_capacity{resource="cpu"})
# Rechercher des PODS Kubernetes non sains (statut pending/unknown/failed)
min_over_time(sum by (namespace, pod) (kube_pod_status_phase{phase=~"Pending|Unknown|Failed"})[15m:1m]) > 0
# Rechercher les PODS sans limite CPU 
count by (namespace)(sum by (namespace,pod,container)(kube_pod_container_info{container!=""}) unless sum by (namespace,pod,container)(kube_pod_container_resource_limits{resource="cpu"}))
# Rechercher PersistentVolumeClaim (PVC) dans l'état d'attente (non alloué a un PerssistentVolume (PV))
kube_persistentvolumeclaim_status_phase{phase="Pending"}
# Rechercher des nœuds instables (bascule trop fréquente entre ready/not ready)
sum(changes(kube_node_status_condition{status="true",condition="Ready"}[15m])) by (node) > 2
# Rechercher les cœurs de processeur inactifs
sum((rate(container_cpu_usage_seconds_total{container!="POD",container!=""}[30m]) - on (namespace,pod,container) group_left avg by (namespace,pod,container)(kube_pod_container_resource_requests{resource="cpu"})) * -1 >0)
# Rechercher la mémoire inactive
sum((container_memory_usage_bytes{container!="POD",container!=""} - on (namespace,pod,container) avg by (namespace,pod,container)(kube_pod_container_resource_requests{resource="memory"})) * -1 >0 ) / (1024*1024*1024)
# Rechercher l'état du nœud
sum(kube_node_status_condition{condition="Ready",status="true"}) # statut "Ready
sum(kube_node_status_condition{condition="NotReady",status="true"}) # statut "NotReady"
sum(kube_node_spec_unschedulable) by (node) # Les noeuds sur lesquels nous ne pouvons exécuter des Pods
```
