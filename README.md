# vt
All Voting Terminal services started from a single repository with docker-compose.

## Download from github
```
git clone --recurse-submodules https://github.com/tp17-2021/vt
cd vt
```

## Pulling changes
```
git checkout development
git pull --recurse-submodules
cd backend
git pull
git checkout EV-102-development
cd ..
cd frontend
git checkout development
git pull
cd ..
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
nano docker-compose-html-external.yml
```
(paste path to "volumes")


## Starting docker for development
```
sudo service docker start
docker-compose -f docker-compose-html-external.yml up -d --build
```
(backend server will now be running on http://localhost:81/)

### to build svelte frontend with hot reloading
```
npm i
npm run dev
```
(svelte frontend is now running at http://localhost:5000/)

### to build svelte frontend without hot reloading using docker:
```
cd frontend
docker build -t sveltefrontend .
docker run --rm --name sveltefrontendc -p 5000:80 sveltefrontend
```

## Gateway needs to be running for backend to work correctly
use instructions from https://github.com/tp17-2021/gateway/tree/development#usage to set it up
