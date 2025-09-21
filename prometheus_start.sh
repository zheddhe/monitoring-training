#!/usr/bin/env bash
prometheus/prometheus --config.file=${1:-prometheus.yml}