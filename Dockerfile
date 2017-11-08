FROM ubuntu:14.04

RUN apt-get update -y
RUN apt-get install -y --fix-missing build-essential 
RUN apt-get install -y --fix-missing gcc 
RUN apt-get install -y --fix-missing python-dev 
RUN apt-get install -y --fix-missing python-pip 
RUN apt-get install -y --fix-missing libmysqlclient-dev 
RUN apt-get install -y --fix-missing git  
RUN apt-get install -y --fix-missing wget 
RUN apt-get install -y --fix-missing unzip 
RUN apt-get install -y --fix-missing firefox
RUN apt-get install -y --fix-missing xvfb 
#libglib2.0-0 libxi6 libgconf-2-4 ibglib2.0-0 libxss1 libgconf-2-4 libnss3 libfontconfig libX11.6 



RUN pip install --upgrade pip
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

WORKDIR /app

ENV PATH="/app:${PATH}"

# move above pip
COPY chrome.sh /app/chrome.sh
RUN sh /app/chrome.sh


COPY . /app/
COPY auth /auth/

ENV PYTHONPATH /app/

ENTRYPOINT ["python"]

CMD ["main.py"]