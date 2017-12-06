# PathISTabs
A program that dumps Natural Language Search text/PDF results into spreadsheet tabular and json formats. 

## README for non-developers

The webapp program is multi-platform and has been tested on the following systems (Windows 10, Ubuntu 16.04 and MacOS Sierra).

### Download repository

Repository:
https://github.com/gcampuzano14/PathISTabs

> Green button "Clone or download" (top right)
> > Download zip

Extract contents to preferred folder (i.e. Desktop, Documents, etc.). You should have a path like this (root path for application): `C:\Peferred_folder\PathISTabs`.

### Windows-specific instructions


#### Check python version

You need python 3.5+ to run this program. Version should be 3.5 (tested version) but may run on Python 3.6. This version hasn't been tested on Python 2x.

Access Windows command prompt (**CMD**) as administrator from within the PathISTabs parent directory (PathISTabs) (http://www.thewindowsclub.com/how-to-run-command-prompt-as-an-administrator)

Type the following command inside the CMD:

> python

If python is installed i your system you should see something like this: 
`Python 3.5.2 (v3.5.2:4def2a2901a5, Jun 25 2016, 22:18:55) [MSC v.1900 64 bit (AMD64)] on win32`

If installed, take note of the version; it should be 3.5.x (see below for further explanation). 

If python is not installed i your system you will get a message similar or equal to this: 
`'python' is not recognized as an internal or external command operable program or batch file`

Exit the python console with `control+c` or type `exit()`

If no python version is installed or the version is python 2.7 you will need to get and install python 3.5.3 (https://www.python.org/downloads/release/python-353/). 
**Download links:**
- Python 3.5.3 (64 bits): https://www.python.org/ftp/python/3.5.3/python-3.5.3-amd64.exe
- Python 3.5.3 (32 bits): https://www.python.org/ftp/python/3.5.3/python-3.5.3.exe

Execute `python-3.5.3.exe` setup file and follow setup instructions.
> First setup screen  
> > Bottom, select `Add Python 3.5 to PATH`  
> > Leave all other options as they are  
> > Select: `Install Now` option  
>
> Let installation finish and hit `close` button  

Open a new CMD and verify installation by typing following command:

> python

Results should be as stated above in previous section, something like this:
`Python 3.5.2 (v3.5.2:4def2a2901a5, Jun 25 2016, 22:18:55) [MSC v.1900 64 bit (AMD64)] on win32`


#### Setup python virtual environment

Once python is installed, within the and still inside a new CMD, inside the program's root folder (PathISTabs) you need to setup a virtual environment:

- Install virtualenv

If default python is 3+
> pip install virtualenv

If default python is not 3+ 
> pip3 install virtualenv

Create virtual environment
> virtualenv venv

Activate virtualenvironmetn
> venv\Scripts\activate

#### Start application

-clean placeholders
go to webapp\temp\lock folder an delete "placeholder" file

- In CMD (inside program folder) go to webapp folder

> cd webapp

- Start app

> python pathis_nls_parser.py


#### Access app in browser 

- Use chrome or firefox

in the address bar type the following

> 127.0.0.1:5000



