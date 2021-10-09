@echo off
set /p filepath=What's the file path/file name: 
python mpkunpack.py %filepath%
pause