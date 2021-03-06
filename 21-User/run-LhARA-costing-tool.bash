#!/bin/bash
#set -e
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

#..  Set virtual environment
source ./venv/bin/activate
if [ $debug == "true" ]; then
    echo "Virtual environment set:"
    test=$(which python)
    echo "    which python:" $test
fi
 
#-------- Execute LhARA costing tool start  --------  --------  --------  

python3 $LhARAPATH/04-Scripts/run-LhARA-costing-tool.py "Debug=$debug"
