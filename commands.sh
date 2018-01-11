cd unsubscribe; git pull; cd ..

docker build -t master .
docker build -f Dockerfile_slave -t slave .
docker build -f Dockerfile_analytics -t analytics .

docker rm -f $(docker ps -aq); docker run --restart always -t master   &
docker run --restart always -t slave  &


docker run -t analytics &


vim /etc/rc.local
cd /home/wdvorak; sudo docker build -t master . 
cd /home/wdvorak; sudo docker rm -f $(docker ps -aq)
cd /home/wdvorak; sudo docker build -f Dockerfile_slave -t slave .
cd /home/wdvorak; sudo docker run --restart always -t master &
cd /home/wdvorak; sudo docker run --restart always -t slave &

export VISUAL=vim
crontab -e

SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

* */2 * * * sudo gcloud compute --project "hosting-2718" instances stop --zone "us-east1-d" "unsub"; sudo gcloud compute --project "hosting-2718" instances start --zone "us-east1-d" "unsub"