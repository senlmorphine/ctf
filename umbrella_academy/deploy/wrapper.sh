#! /bin/bash

cd /home/umbrella_academy

# standard version (hard)
timeout 30 ./umbrella_academy-O2 0.  ||  echo "Timeout"
