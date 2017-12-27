REM should only have to do this once
git lfs install
git lfs track 'installers/*.exe'
git lfs track 'installers/*.zip'
REM look at what lfs is tracking
git lfs track
REM add the files we want to put into github lfs
git add .gitattributes "installers\*.exe"
git add .gitattributes "installers\*.zip"
git status
git lfs ls-files
REM now you can do
REM git commit
REM git push
REM sometimes it is better from the console instead of PyCharm since you can see real time status
