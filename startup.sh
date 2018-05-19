apt-get update -y
apt-get install -y --fix-missing build-essential 
apt-get install -y --fix-missing gcc 
apt-get install -y --fix-missing python-dev 
apt-get install -y --fix-missing python-pip 
apt-get install -y --fix-missing libmysqlclient-dev 
apt-get install -y --fix-missing git  
apt-get install -y --fix-missing wget 
apt-get install -y --fix-missing unzip 
apt-get install -y --fix-missing firefox
apt-get install -y --fix-missing xvfb 
apt-get install -y --fix-missing tar

mkdir /app
export PATH="/app:${PATH}"

cd /app

git clone https://github.com/skier31415/unsubscribe
git clone https://skier31415:password@github.com/skier31415/auth

cp unsubscribe/geckodriver.sh /app/geckodriver.sh
sh /app/geckodriver.sh

cp unsubscribe/requirements.txt /app/requirements.txt
pip install -r /app/requirements.txt



cp unsubscribe/source/ /app/
cp auth /auth/

export PYTHONPATH="/app/"

echo "$(cat /app/main.py)\nmainSlave()" > /app/main.py

python main.py
