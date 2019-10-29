#!/bin/bash

echo "Checking for untracked files"
var=$(git ls-files . --exclude-standard --others -m)
if [ -z "$var" ]; then
	echo "There is nothing."
else
	echo "There is something."
fi
