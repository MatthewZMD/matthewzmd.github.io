#!/bin/bash

if [ $# -lt 2 ]
  then
      echo "Usage: raw_filter.sh RAW_FOLDER JPEG_FOLDER_1 JPEG_FOLDER_2"
      exit 1
fi

raws=`ls $1 | egrep '\.ARW$|\.DNG$|\.RAF$'`
jpegs=`ls $2 | egrep '\.JPG$|\.jpg$|\.jpeg$|\.JPEG$'`
if [ $# -eq 3 ]
  then
      jpegs_2=`ls $3 | egrep '\.JPG$|\.jpg$|\.jpeg$|\.JPEG$'`
fi

keep_raw=""
delete_raw=""

for raw in $raws
do
    raw_noex="${raw%.*}"
    echo $raw_noex
    if [[ $jpegs == *$raw_noex* ]]; then
        echo $raw " Found!"
        keep_raw="$raw $keep_raw"
        cp $1/$raw $2/$raw
    elif [[ $# -eq 3 && $jpegs_2 == *$raw_noex* ]]; then
        echo $raw " Found!"
        keep_raw="$raw $keep_raw"
        cp $1/$raw $3/$raw
    else
        delete_raw="$raw $delete_raw"
    fi
done

if [ -z "$keep_raw" ]; then
    echo "No raws to keep, make sure folders are correct!"
    exit 1
elif [ -n "$delete_raw" ]; then
    for r in $delete_raw
    do
        echo "Removing:" $r
        rm -rf $1/$r
    done
fi
