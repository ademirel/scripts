#!/bin/bash

# Usage: takeover.sh pardus/devel/kernel/kernel/pspec.xml

NAME="YOUR NAME"
EMAIL="YOUR EMAIL"

sed -i "/<Packager>$/{
N
N
N
s/<Name>.*<\/Name>\n/<Name>$NAME<\/Name>\n/
s/<Email>.*<\/Email>\n/<Email>$EMAIL<\/Email>\n/
}" $1