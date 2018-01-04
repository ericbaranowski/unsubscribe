docker build -t master .
docker rm -f $(docker ps -aq); docker run -t master &

docker build -f Dockerfile_slave -t slave .
docker run -t slave &

docker build -f Dockerfile_analytics -t analytics .
docker run -t analytics &