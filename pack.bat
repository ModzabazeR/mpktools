@echo off
set /p tocpath=What's the TOC path / TOC name: 
set /p filepath=Name your .mpk file: 
python mpkpack.py %tocpath% %filepath%
pause