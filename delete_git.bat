@echo off

SET /p branch=Enter branch name to delete:

echo Switching to 'master' branch..
git checkout master

echo Deleting local branch..
git branch -d %branch%

echo Deleting remote branch..
git push origin :%branch%

echo '%branch%' deleted on both local and remote.