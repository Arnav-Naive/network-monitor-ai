#!/bin/sh
echo $((35 + $(od -An -N2 -tu2 /dev/urandom) % 41))