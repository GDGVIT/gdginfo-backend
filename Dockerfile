FROM python:3.6

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

# apt-get because apt doesnt have a stable CLI for debian buster
RUN apt-get update && apt-get upgrade -y && apt-get install build-essential

COPY . . 

RUN . /usr/src/app/.env

RUN make

# EXPOSE 3000

# -u flag to use unbuffered output
# Cannot use --with-cache on heroku as
# PORT bind time increases
ENTRYPOINT ["python3", "-u", "/usr/src/app/app"]

