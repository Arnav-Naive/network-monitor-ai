#!/bin/sh
echo $((40 + $(od -An -N2 -tu2 /dev/urandom) % 51))