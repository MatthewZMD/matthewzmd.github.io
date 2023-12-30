#!/bin/bash

# $1: year, $2: months / all monthss if omitted

function optimize() {
    jpegoptim -o --strip-exif -p -P -S1900 $1
    convert $1 -gravity South -pointsize 30 -font Helvetica -fill "#cee3f8" -annotate +1+50 "(C) Ming De Zeng" $1
    convert $1 -thumbnail 250x250 +repage -unsharp 0x.5 -quality 80 $2
}

gallery_dir=$(git rev-parse --show-toplevel)/gallery

if [ -z "$1" ]
then
    echo "Please specify a year!"
    exit 1
fi

selected_file=""

if [ -z "$2" ]
then
    months="01 02 03 04 05 06 07 08 09 10 11 12"
elif [ -n $3 ] && [[ $3 == *.jpg ]]; then
    months=$2
    selected_file=$3
else
    months="${@:2}"
fi

for month in $months
do
    full_path=$gallery_dir/full/$1/$month
    thumb_path=$gallery_dir/thumbnail/$1/$month
    [ -d $full_path ] && mkdir -p $thumb_path
    if [ -n "$selected_file" ] && [ -f "$full_path/$selected_file" ]; then
        optimize $full_path/$selected_file $thumb_path/$selected_file
    else
        if command -v fdfind &> /dev/null; then
            FIND=fdfind
        elif command -v fd &> /dev/null; then
            FIND=fd
        fi
        FILES=$($FIND --extension jpeg --extension jpg --full-path $full_path)
        for FILE in $FILES
        do
            if [[ "$FILE" == *.jpeg ]]; then
                echo "Renaming" $FILE to ${FILE%.jpeg}.jpg
                mv "$FILE" "${FILE%.jpeg}.jpg"
                FILE="${FILE%.jpeg}.jpg"
            fi
            optimize $FILE $thumb_path/$(basename $FILE)
        done
    fi
done
