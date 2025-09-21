#!/usr/bin/env bash
# ${@:2} tous les argument additionnels après le premier sont passés à la commande
prometheus/prometheus --config.file=${1:-config/prometheus.yml} ${@:2}