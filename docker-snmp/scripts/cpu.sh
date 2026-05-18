#!/bin/sh
MIN=${CPU_MIN:-40}
MAX=${CPU_MAX:-90}
RANGE=$((MAX - MIN))
echo $((MIN + $(od -An -N2 -tu2 /dev/urandom) % RANGE))