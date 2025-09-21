#!/usr/bin/env bash
prometheus/promtool check rules ${1:-recording_rules.yml}