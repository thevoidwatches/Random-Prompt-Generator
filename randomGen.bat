@echo off
:randselect
echo How many prompts would you like to generate?
set /p rand= 
python randomGen.py -if promptSource.txt -of prompts.txt -v -r %rand% -l
echo:
echo Enter r to rerun, or anything else to close.
set /p go=
if %go% == r (
    goto:randselect
)