#!/bin/bash
set -e
set -u

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
    echo "LhARA costing tool run from director:"
    echo "    " $HOMEPATH
fi
export HOMEPATH

LhARAPATH="/Users/kennethlong/CubMac-Home/CCAP/18-LhARA/00-Admin/01-Costing/01-LhARA-costing-tool"
if [ $debug == "true" ]; then
    echo "LhARA path set:"
    echo "    " $LhARAPATH
fi

add="/01-Code"
dir="$LhARAPATH$add"
if [ -z ${PYTHONPATH+x} ]; then
    PYTHONPATH="$dir"
else
    PYTHONPATH="${PYTHONPATH}:$dir"
fi
if [ $debug == "true" ]; then
    echo "Python path set:"
    echo "    " $PYTHONPATH
fi
export PYTHONPATH

add="/Reports"
REPORTPATH="$HOMEPATH$add"
if [ $debug == "true" ]; then
    echo "Reports path set:"
    echo "    " $REPORTPATH
fi
export REPORTPATH

#-------- Execute LhARA costing tool start  --------  --------  --------  

python3 $LhARAPATH/04-Scripts/run-LhARA-costing-tool.py "Debug=$debug"
