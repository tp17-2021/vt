# Voting Terminal


## Gateway needs to be running for backend to work correctly

Datamodel.yaml is downloaded from Gateway and `src/schemas/votes.py` is generated before server is started. Gateway must run at the time so datamodel cen be found.

The second thing is that backend server itself needs to be able to connect to Gateway on startup to register itself and get `id` and Gateway's `public_key`.


## Running docker in regular way (backend development e.g.)
```
docker-compose up -d --build
```


## Running test in docker
```
docker-compose -f docker-compose.test.backend.yml up --build
```


## Ports

VT runs on port `81` in development by default. This can be changed in `docker-compose.yml`.

Backend is served on `/backend` and Fast API GUI can be found on `/backend/docs` (full path: `http://localhost:81/backend/docs`)

Frontend is served on directly on root (`http://localhost:81/`).
 


## Download from github
```
git clone git@github.com:tp17-2021/vt.git
cd vt
```

## Pulling changes
```
git pull
```


## Fronted development related bellow

### Configuring svelte hot reloading for development
```
cd frontend
cd public
pwd
```
(copy path)
```
cd ..
cd ..
nano docker-compose.dev.yml
```
(paste path to "volumes")


### Starting docker for frontend development
```
sudo service docker start
docker-compose -f docker-compose.dev.yml up -d --build
```
(backend server will now be running on `http://localhost:81/`)


