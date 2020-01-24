FROM python:3.6

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

RUN apt-get update && apt-get upgrade -y && apt-get install libcurl4-gnutls-dev python-setuptools -y

RUN wget -O gitinspector.deb https://github.com/ejwa/gitinspector/releases/download/v0.4.3/gitinspector_0.4.3-1_all.deb && dpkg -i gitinspector.deb

COPY . . 

RUN pip3 install -r requirements.txt

RUN . /usr/src/app/.env

RUN chmod +x app

# EXPOSE 3000

# -u flag to use unbuffered output
# Cannot use --with-cache on heroku as
# PORT bind time increases
ENTRYPOINT ["python3", "-u", "/usr/src/app/app"]

