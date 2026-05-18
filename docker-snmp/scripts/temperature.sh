#!/bin/sh
MIN=${TEMP_MIN:-35}
MAX=${TEMP_MAX:-75}
RANGE=$((MAX - MIN))
echo $((MIN + $(od -An -N2 -tu2 /dev/urandom) % RANGE))