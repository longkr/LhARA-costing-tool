#!/bin/bash

stm=$PWD
#echo $stm

dir="$stm"
echo "Set LhARA path:"
LhARAPATH="$dir"
echo "    " $LhARAPATH
export LhARAPATH

add="/01-Code"
#echo $add
dir="$stm$add"
#echo $dir
echo "Set PYTHON path:"
PYTHONPATH="${PYTHONPATH}:$dir"
echo "    " $PYTHONPATH
export PYTHONPATH
