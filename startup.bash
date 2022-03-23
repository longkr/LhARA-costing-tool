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

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
LhARAPATH=$SCRIPT_DIR
if [ $debug == "true" ]; then
    echo "LhARA path set:"
    echo "    " $LhARAPATH
fi
export LhARAPATH

add="/01-Code"
dir="$LhARAPATH$add"
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
