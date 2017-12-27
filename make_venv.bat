"C:\Program Files\Python36\python.exe" -m venv --clear venv
venv\Scripts\pip3 install -U pip
venv\Scripts\pip3 install -U setuptools
REM use the latest osnap in the directory next to this one
venv\Scripts\pip3 install -U --find-links ..\osnap\dist -r requirements.txt
