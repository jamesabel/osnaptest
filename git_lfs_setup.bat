REM should only have to do this once
git lfs install
git lfs track "installers/*.*"
REM see what we did
git lfs track
git add .gitattributes
git status
git lfs ls-files
REM now you can do
REM git commit
REM git push
REM sometimes it is better from the console instead of PyCharm since you can see real time status
