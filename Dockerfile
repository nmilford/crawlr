FROM ubuntu
MAINTAINER Nathan Milford <nathan@milford.io>
RUN apt-get update
RUN apt-get install -y \
            python-pip \
            python-dev \
            libev4 \
            libev-dev 
#            build-essential \
#            git 
ADD . /crawlr

RUN pip install -r /crawlr/requirements.txt
WORKDIR /crawlr
EXPOSE 5000
CMD ./bin/crawlr-api
