#!/bin/bash
# _IN_FILE=
cp $_IN_FILE ./tmp.txt
python gao.py | grep -v -e "^$" > stdout.log
rm ./tmp.txt
echo 'Done'

