@echo off

SET /p branch=Enter branch name:

echo Creating local branch..
git checkout -b %branch%

echo Pushing local branch '%branch%' to remote origin..
git push origin %branch%

echo '%branch%' successfully created on local and remote.
echo You're now in '%branch%' branch.