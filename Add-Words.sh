#!/bin/bash
. Config/Config.sh
head -n $1 $FILE_FROM | tee /dev/tty | python3 Translate.py $API_KEY $LANG | tee -a $FILE_TO
tail -n +$[$1 + 1] $FILE_FROM | tee $FILE_FROM > /dev/null

