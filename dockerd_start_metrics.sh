#!/bin/bash
sudo dockerd --experimental --metrics-addr=127.0.0.1:9323 & disown