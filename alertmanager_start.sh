#!/usr/bin/env bash
alertmanager/alertmanager --config.file=${1:-config/alertmanager.yml} ${@:2}