#!/bin/bash

#-------- Initialisation  --------  --------  --------  --------  --------

#.. Parse arguments:
debug="false"
while getopts "d" opt; do
    case $opt in
	d) debug="true" ;;
    esac
done

#.. Set environment variables:
HOMEPATH=$PWD
if [ $debug == "true" ]; then
    echo "LhARA costing tool run from directory:"
    echo "    " $HOMEPATH
fi
export HOMEPATH

LhARAPATH=$HOMEPATH
if [ $debug == "true" ]; then
    echo "LhARA path set:"
    echo "    " $LhARAPATH
fi
export LhARAPATH

add="/01-Code"
dir="$LhARAPATH$add"
echo $dir
if [ -z ${PYTHONPATH+x} ]; then
    echo $dir
    PYTHONPATH=":$dir"
else
    PYTHONPATH="${PYTHONPATH}:$dir"
fi
if [ $debug == "true" ]; then
    echo "Python path set:"
    echo "    " $PYTHONPATH
fi
export PYTHONPATH

add="/99-Scratch"
REPORTPATH="$HOMEPATH$add"
if [ $debug == "true" ]; then
    echo "Reports path set:"
    echo "    " $REPORTPATH
fi
export REPORTPATH
