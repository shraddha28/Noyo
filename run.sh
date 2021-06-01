#!/bin/bash

#Install required dependencies
pip install -r requirements.txt

#Run the application
ver=$(python -c"import sys; print(sys.version_info.major)")
if [ $ver -eq 2 ]; then
    echo "python version 2"
    python3 noyo_run.py
elif [ $ver -eq 3 ]; then
    echo "python version 3"
    python noyo_run.py
else 
    echo "Python not installed. *Please install python before running this script*"
fi
