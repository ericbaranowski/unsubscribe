docker build -t latest .
docker rm -f $(docker ps -aq); docker run -t latest