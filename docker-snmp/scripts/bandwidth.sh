#!/bin/sh
echo $((200 + $(od -An -N2 -tu2 /dev/urandom) % 701))