# Reference DB
This repository containes the python code that was used to develop an internal tool at the FH WN, campus Tulln. 
The aim of the project was to create a database and webinterface that allows the storage and querying of surface-enhanced raman spectra. 
The project was realized by Lukas Steininger with python flask as a server side rendering backend and html for the template files. 

## Setup
In order to use this tool you need to download the repository. 
The repo holds the required packages for the conda environment in the file _requirements.txt_\
You can do so by using this commmand:\
   CONDA CREATE --NAME <ENV> --FILE REQUIREMENTS.TXT\
The entry point of the application is the file start.py which needs 
to be started accordingly. By default the programm creates a sqlite database file called _app.db_ located in the root directory. Stored spectra in the
csv format are store in a directory called _appdata_ also located in the root directory. 

## Interaction
### Authentication
The database only allows authenicated users to acces and alter its data. Thus the webapp provides functionality for signing up and login in. 
Additionaly admins can activate, deactivate or delete users completly.

### Ressource administration
Resources which can be used for meassuring a compound, can and should be administored. This takes away sources of errors when
crearting a new compound, since the user has to choose from available options.

### Adding of compounds
A compound holds all the information of its measurment (date, user, lenses, ...) and also the data points of the spectra itself.
These spectra are then used to query the database agains a given set of wavenumbers.

### Querying of compounds
The user can use a set of wavenumbers and tolerance value (applied to all wavenumbers) to query all available spectra. If a spectrum contains any of the specified wavenumbers, it is classified as a match. 
All the matches are grouped and returned to the user in order to allow further interaction and interpretation.
