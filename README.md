# vt
All Voting Terminal services started from a single repository with docker-compose.

## Download from github
```
git clone git@github.com:tp17-2021/vt.git
cd vt
```

## Pulling changes
```
git pull
```

## Running docker in regular way (backend development e.g.)
```
docker-compose up -d --build
```


## Configuring svelte hot reloading for development
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


## Starting docker for frontend development
```
sudo service docker start
docker-compose -f docker-compose.dev.yml up -d --build
```
(backend server will now be running on http://localhost:81/)


## Gateway needs to be running for backend to work correctly
use instructions from https://github.com/tp17-2021/gateway/tree/development#usage to set it up. After running the backend, in the docker logs you should see the message that connection to gateway is succesfull.
