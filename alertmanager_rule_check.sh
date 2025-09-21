#!/usr/bin/env bash
alertmanager/amtool check-config ${1:-config/alertmanager.yml}