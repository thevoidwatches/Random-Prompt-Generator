@echo off
:start
python randomGen.py -if promptSource.txt -of prompts.txt -v -t -l
echo:
echo Enter r to rerun, or anything else to close.
set /p go=
if %go% == r (
    goto:start
)