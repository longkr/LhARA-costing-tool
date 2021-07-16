#!/bin/bash
#
#..  Integration test script.  Runs each test and creates integrated log
#    file.  Check of log file constitutes the test.  
#
#..  Assumes "startup.bash" has been run.

cd $LhARAPATH
02-Tests/WorkPackageTst.py   > 99-Scratch/WorkPackageTst.log
02-Tests/TaskTst.py          > 99-Scratch/TaskTst.log
02-Tests/StaffTst.py         > 99-Scratch/StaffTst.log
02-Tests/ProjectTst.py       > 99-Scratch/ProjectTst.log
02-Tests/EquipmentTst.py     > 99-Scratch/EquipmentTst.log
02-Tests/TaskStaffTst.py     > 99-Scratch/TaskStaffTst.log
02-Tests/TaskEquipmentTst.py > 99-Scratch/TaskEquipmentTst.log

02-Tests/ReportTst.py        > 99-Scratch/ReportTst.log

cat 99-Scratch/*Tst.log > 99-Scratch/AllTst-log.txt

DIFF=$(diff 99-Scratch/AllTst-log.txt 03-Integration-test/Integration-test-reference-log.txt)

length=${#DIFF}
if [ $length == 0 ]
then
    echo " ----> Integration test succeeded <----"    
else
    echo " ----> Integration test FAILED!! <----"
fi
