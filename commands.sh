docker build -t latest .
docker rm -f $(docker ps -aq); docker run -t latest


docker build -f Dockerfile_slave -t latest .
docker rm -f $(docker ps -aq); docker run -t latest