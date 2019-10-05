# billboard-viewer
A web app to view data retrieved by the reader

### Installation
Install (pipenv)[https://www.pipenv.org]

pipenv run application.py

Create the docker file and run with a env_file
env_file should have
DATABASE
DB_TYPE
DB_USERNAME
DB_HOST=<host:port>
PASS

`docker run env-file=env_file -p 5000:5000 <container-name>:<container-tag>`