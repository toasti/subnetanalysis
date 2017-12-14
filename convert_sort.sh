#!/bin/sh

head -n 1 "$1" > "$1_temp" && tail -n +2 "$1" | sort -t "," -k 1 >> "$1_temp"

mv "$1_temp" "$1"
