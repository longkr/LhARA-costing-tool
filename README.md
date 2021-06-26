# LhARA costing tool

The code in this repository provides python code to automate the compilation of the costs for the LhARA project.  

## To set up and run:
A guide to setting up and running the LhARA costing tool will be provided.  However, to get going:
 * Execute "startup.bash" from this directory (i.e. run the bash command "source startup.bash").  This will:
  * Set up "nuSIMPATH"; and
  * Add "01-Code" to the PYTHONPATH.  The scripts in "02-Tests" may then be run with the command "python 02-Tests/<filename>.py".

## Directories:
 * Python classes and "library" code stored in "01-Code"
 * Test scripts stored in "02-Tests"
 * An integration test is provided in 03-Integration-test
 * And scripts are collected in 04-Scripts
 * Workpackage definitions (input) are collected in 11-Workpackages
 * The staff data base is stored in 12-Staff
 * 99-Scratch is provided as a scratch directory.

Rudimentary, but, goal is one test script per class/package file in 01-Code.

## Dependencies:
 * Code and test scripts assume Python 3.  
 * Test scripts assume code directory (01-Code) is in PYTHON path.  A bash script "startup.bash" is provided to update the PYTHON path.
