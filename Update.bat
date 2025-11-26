@echo off
Title Git Updater
echo You must have git installed and on PATH to use the update script. Continue if this is fine, die if it is not
pause
git init
git pull https://github.com/MokyNZZ/RoR2-Save-Editor
echo Done updating!
pause