#!/bin/sh
echo $((50 + $(od -An -N2 -tu2 /dev/urandom) % 36))