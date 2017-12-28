docker build -t latest .
docker rm -f $(docker ps -aq); docker run -t latest


docker build -f Dockerfile_slave -t latest .
docker run -t latest


docker build -f Dockerfile_analytics -t latest .
docker run -t latest