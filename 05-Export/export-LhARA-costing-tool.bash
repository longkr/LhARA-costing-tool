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
    echo "Export LhARA costing tool to new HOME directory:"
    echo "    " $HOMEPATH
fi
export HOMEPATH

BaseDir=$(dirname "$0")
LhARAPATH=$(dirname $BaseDir)
if [ $debug == "true" ]; then
    echo "LhARA path set:"
    echo "    " $LhARAPATH
fi

#-------- Installation  --------  --------  --------  --------  --------

#.. Parse arguments:
add="/21-User"
UserPATH="$LhARAPATH$add"
if [ $debug == "true" ]; then
    echo "Copying from:"
    echo "    " $UserPATH
fi
cp -r $UserPATH/* .

search='LhARAPATH="/Users/kennethlong/CubMac-Home/CCAP/18-LhARA/00-Admin/01-Costing/01-LhARA-costing-tool"'
replace='LhARAPATH="'$LhARAPATH'"'
filename=run-LhARA-costing-tool.bash
if [ $debug == "true" ]; then
    echo "Changing LhARAPATH from:"
    echo "    " $search
    echo "to:"
    echo "    " $replace
fi
sed "s+$search+$replace+g" $filename > temp
mv temp $filename
chmod +x $filename
