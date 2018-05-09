#SHELL=/bin/sh
#PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
# 1 6 * * * python /home/wdvorak/unsubscribe/source/removeDockerCruft.py

def removeDockerCruft():
  import os
  os.system('rm -rf /var/lib/docker/aufs')
  os.system('service docker restart')
  os.system('cd /home/wdvorak/;docker build -t master .')
  os.system('cd /home/wdvorak/;docker build -f Dockerfile_slave -t slave .')
  os.system('docker rm -f $(docker ps -aq)')
  os.system('docker run --restart always -t master   &')
  os.system('docker run --restart always -t slave  &')
  os.system('docker run --restart always -t slave  &')
  
removeDockerCruft()