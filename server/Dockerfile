FROM ubuntu:latest

RUN apt update && apt install -y libpcre3-dbg \
                                    libpcre3-dev \
                                    autoconf \
                                    automake \
                                    libtool \
                                    libpcap-dev \
                                    libnet1-dev \
                                    libyaml-dev \
                                    libjansson4 \
                                    libcap-ng-dev \
                                    libmagic-dev \ 
                                    libjansson-dev \
                                    zlib1g-dev \
                                    python3-pip \
                                    software-properties-common

RUN add-apt-repository ppa:oisf/suricata-stable && apt update -y && apt install -y suricata

RUN mkdir /ctf

COPY serve.py /ctf/
COPY flag.txt /ctf/
COPY expected.json /ctf/
COPY pcaps/ /ctf/pcaps

RUN groupadd ctf
RUN useradd -G ctf --home=/ctf ctfuser
RUN chown -R ctfuser:ctfuser /ctf

EXPOSE 9999

ENTRYPOINT ["su", "-c", "python3 /ctf/serve.py", "-", "ctfuser"]
