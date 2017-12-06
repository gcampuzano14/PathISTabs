# PathISTabs
A program that dumps Natural Language Search text/PDF results into spreadsheet tabular format. 

## README for non devs

## Run on Windows (tested on Windows 10)

### Download repository

Repository:
https://github.com/gcampuzano14/PathISTabs

> Button "Clone or download"
> > Download zip

Extract contents to prefered folder

### Check python version

You need python 3.5+ to run this program. Version should be 3.5 (tested version) but may run on Python 3.6.

Access Windows command prompt (CMD) as administrator from within the progrma parent directory (PathISTabs) (http://www.thewindowsclub.com/how-to-run-command-prompt-as-an-administrator)

type the following command:

> python

You should see something like this: 
Python 3.5.2 (v3.5.2:4def2a2901a5, Jun 25 2016, 22:18:55) [MSC v.1900 64 bit (AMD64)] on win32

exit the python console with control+c

If no python version is installed or the version is python 2.7 you will need to install get and install python 3.5 (https://www.python.org/downloads/release/python-350/)

## Setup python virtualenvironment

Once python is installed, and still inside the command prompt inside the progams root folder you need to set up a virtualenvironment:

- Install virtual env

If default python is 3+
> pip install virtualenv

If default python is not 3+ 
> pip3 install virtualenv

Create virtual environment
> virtualenv venv

Activate virtualenvironmetn
> venv\Scripts\activate

### Start application

-clean placeholders
go to webapp\temp\lock folder an delete "placeholder" file

- In CMD (inside program folder) go to webapp folder

> cd webapp

- Start app

> python pathis_nls_parser.py


### Access app in browser 

- Use chrome or firefox

in the address bar type the following

> 127.0.0.1:5000



