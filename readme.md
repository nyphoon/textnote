# How to run it
* To run this textnote application, Python 3.5 or above is required.
* Run in virtualenv is suggested

## Ubuntu steps
* setup virtualenv
```
sudo apt-get install python3-venv
python3 -m venv env
source ./env/bin/activate
```
* setup service
```
cd {THIS DIRECTORY}
pip install -r requirements.txt
export FLASK_APP=textnote
export FLASK_ENV=development
flask init-db
```
* start on port 8080
```
flask run --port=8080
```
* open applicaon [http://localhost:8080](http://localhost:8080)
## Windows steps
* setup virtualenv
```
pip install virtualenv
python3 -m venv env
env\Scripts\activate.bat
```
* setup service
```
cd {THIS DIRECTORY}
pip install -r requirements.txt
set FLASK_APP=textnote
set FLASK_ENV=development
flask init-db
```
* start on port 8080
```
flask run --port=8080
```
* open applicaon [http://localhost:8080](http://localhost:8080)