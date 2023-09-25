# Reference DB

This repository containes the python code that was used to develop an internal tool at the FH WN, campus Tulln.
The aim of the project was to create a database and webinterface that allows the storage and querying of
surface-enhanced raman spectra.
The project was realized by Lukas Steininger with python flask as a server side rendering backend and html for the
template files.

## Setup

In order to use this tool you need to download the repository.

### Conda

Conda is a tool for managing dependencies and virtual environments.
The file **requirements.txt** holds the required packages for the conda environment\
You can create a conda environment with the required packages by using this command:\
`conda create --name refdb --file requirements.txt`

### Database

The database is a sqlite database. It is a database that uses a .db file to store its entries. No database server is
needed.
The database can be created by running the package **setup**
Running this does a few things:

* creates a database with the name **app.db** in the directory specified in **conf.py**
* adds all the required tables to the database (see models.py)
* adds the default user groups **admin** and **user** to the database
* adds a default admin user to the database
* adds the three default spectra**types to the database

You can run setup with the following command:\
`python -m setup`

### Starting the application

The entry point of the application is the file start.py\
It can be started using the following command\
`python -m start`

By default the programm creates a sqlite database file called **app.db** and stores spectra in a directory called *
*appdata**.
However this can be changed in the file **config.py** by changing the values of the variables **DATABASE** and **APPDATA
**.

## Export and Backup of the data

Since a sqlite database is used, the data can be exported and backed up by
simply copying the database file.
In addition to that, the directory **appdata** needs to be
copied as well, because it contains the spectra.

When moving the application to a new location, the database file and the appdata directory 
both need to in the directory specified in the **config.py** file. By default this is the root directory.


## Interaction

### Authentication

The database only allows authenticated users to access and alter its data. 
Thus, the webapp provides functionality for
signing up and login in. Sign up and login page can be accessed via links on the home page.
Additionally, admins can activate, deactivate or delete users completely.

### Ressource administration

Resources which can be used for measuring a compound, can and should be 
administered. This takes away sources of errors when
creating a new compound, since the user has to choose from available options.

E.g the user can add a new lens to the database. 
This lens can then be used when creating a new compound. 
The user does not have to type in the name of the lens, but can choose from a list of available lenses.

### Adding of compounds

A compound holds all the information of its measurement (date, user, lenses, ...) 
and also the data points of the spectra itself.
The user can add a new compound by filling out a form. 
Spectra can be added by uploading a file either directly or later.
These spectra are then used to query the database against a given set of wave-numbers.

### Querying of compounds

The user can use a set of wave-numbers and tolerance value 
(applied to all wave-numbers) to query all available spectra.
If a spectrum contains any of the specified wave-numbers, 
it is classified as a match.
All the matches are grouped and returned to the user in order to 
allow further interaction and interpretation.
