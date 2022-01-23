#!/bin/bash

# $1: year, $2: months / all monthss if omitted

gallery_dir=$(git rev-parse --show-toplevel)/gallery

if [ -z "$1" ]
then
    echo "Please specify a year!"
    exit 1
fi

if [ -z "$2" ]
then
    months="01 02 03 04 05 06 07 08 09 10 11 12"
else
    months=$2
fi

for month in $months
do
    full_path=$gallery_dir/full/$1/$month
    thumb_path=$gallery_dir/thumbnail/$1/$month
    [ -d $full_path ] && mkdir -p $thumb_path
    for FILE in $(fd --extension jpeg --extension jpg --full-path $full_path)
    do
        # 100% Optimize full files
        jpegoptim -p -P -q $FILE
        # Create Thumbnails
        convert -resize 10% $FILE $thumb_path/$(basename $FILE)
    done
done
