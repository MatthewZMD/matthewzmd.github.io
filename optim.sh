#!/bin/bash

for FILE in $(fd -i 'jpe?g')
do
    jpegoptim -p -P -q --size=1000 $FILE
done
