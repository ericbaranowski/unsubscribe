sudo su
cd unsubscribe; git pull; cd ..
cp unsubscribe/Dockerfile* .

docker build -t master .
docker build -f Dockerfile_slave -t slave .
docker build -f Dockerfile_analytics -t analytics .
docker build -f Dockerfile_local -t local .

docker rm -f $(docker ps -aq); docker run --restart always -t master   &
docker run --restart always -t slave  &
docker run --restart always -t slave  &
docker run --restart always -t slave  &

docker run  -t master  
docker run  -t slave  


docker run -t analytics &


gcloud compute --project=hosting-2718 instances create spot5 --zone=us-east1-d --machine-type=n1-standard-1 --subnet=default --metadata=startup-script-url=gs://startupscript-2718/startup.sh --no-restart-on-failure --maintenance-policy=TERMINATE --preemptible --service-account=182434325615-compute@developer.gserviceaccount.com --scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/trace.append --image=ubuntu-1404-trusty-v20180509 --image-project=ubuntu-os-cloud --boot-disk-size=10GB --boot-disk-type=pd-standard --boot-disk-device-name=spot5


gcloud -q compute --project=hosting-2718 instances create spot5 --zone=us-east1-d --machine-type=n1-standard-1  --metadata=startup-script-url=gs://startupscript-2718/startup.sh --no-restart-on-failure --maintenance-policy=TERMINATE --preemptible --service-account=182434325615-compute@developer.gserviceaccount.com --scopes=https://www.googleapis.com/auth/cloud-platform --image=ubuntu-1404-trusty-v20180509 --image-project=ubuntu-os-cloud --boot-disk-size=10GB --boot-disk-type=pd-standard --boot-disk-device-name=spot5


gcloud -q compute instances delete spot5 --zone=us-east1-d 


0 0 * * *  sudo gcloud -q compute instances delete spot0 --zone=us-east1-d; sudo gcloud -q compute --project=hosting-2718 instances create spot0 --zone=us-east1-d --machine-type=n1-standard-1  --metadata=startup-script-url=gs://startupscript-2718/startup.sh --no-restart-on-failure --maintenance-policy=TERMINATE --preemptible --service-account=182434325615-compute@developer.gserviceaccount.com --scopes=https://www.googleapis.com/auth/cloud-platform --image=ubuntu-1404-trusty-v20180509 --image-project=ubuntu-os-cloud --boot-disk-size=10GB --boot-disk-type=pd-standard --boot-disk-device-name=spot0

0 6 * * *  sudo gcloud -q compute instances delete spot6 --zone=us-east1-d; sudo gcloud -q compute --project=hosting-2718 instances create spot6 --zone=us-east1-d --machine-type=n1-standard-1  --metadata=startup-script-url=gs://startupscript-2718/startup.sh --no-restart-on-failure --maintenance-policy=TERMINATE --preemptible --service-account=182434325615-compute@developer.gserviceaccount.com --scopes=https://www.googleapis.com/auth/cloud-platform --image=ubuntu-1404-trusty-v20180509 --image-project=ubuntu-os-cloud --boot-disk-size=10GB --boot-disk-type=pd-standard --boot-disk-device-name=spot6

0 12 * * *  sudo gcloud -q compute instances delete spot12 --zone=us-east1-d; sudo gcloud -q compute --project=hosting-2718 instances create spot12 --zone=us-east1-d --machine-type=n1-standard-1  --metadata=startup-script-url=gs://startupscript-2718/startup.sh --no-restart-on-failure --maintenance-policy=TERMINATE --preemptible --service-account=182434325615-compute@developer.gserviceaccount.com --scopes=https://www.googleapis.com/auth/cloud-platform --image=ubuntu-1404-trusty-v20180509 --image-project=ubuntu-os-cloud --boot-disk-size=10GB --boot-disk-type=pd-standard --boot-disk-device-name=spot12

0 18 * * * sudo gcloud -q compute instances delete spot18 --zone=us-east1-d; sudo gcloud -q compute --project=hosting-2718 instances create spot18 --zone=us-east1-d --machine-type=n1-standard-1  --metadata=startup-script-url=gs://startupscript-2718/startup.sh --no-restart-on-failure --maintenance-policy=TERMINATE --preemptible --service-account=182434325615-compute@developer.gserviceaccount.com --scopes=https://www.googleapis.com/auth/cloud-platform --image=ubuntu-1404-trusty-v20180509 --image-project=ubuntu-os-cloud --boot-disk-size=10GB --boot-disk-type=pd-standard --boot-disk-device-name=spot18

apt-get install git docker.io
# install gcloud
0 5,11,17,23 * * * sudo gcloud -q compute --project "hosting-2718" instances start --zone "us-east1-d" "unsub2"
# every 23 hours
55 2,8,14,20 * * * sudo gcloud compute --project "hosting-2718" instances stop --zone "us-east1-d" "unsub2"

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


cd unsubscribe; git pull; cd ..
cp unsubscribe/Dockerfile_test .
docker build -f Dockerfile_test -t test .

docker run -t test