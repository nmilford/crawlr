FROM ubuntu
MAINTAINER Nathan Milford <nathan@milford.io>

RUN echo "deb http://debian.datastax.com/community stable main" | sudo tee -a /etc/apt/sources.list.d/cassandra.sources.list
RUN apt-get update
RUN apt-get install -y \
            build-essential
            python-pip
            python-dev
            libev4
            libev-dev
            git
#RUN git clone https://github.com/nmilford/crawlr.git crawlr
ADD /crawlr /crawlr

RUN pip install -r /crawlr/requirements.txt
WORKDIR /crawlr
EXPOSE 5000
CMD ./bin/crawlr-api
