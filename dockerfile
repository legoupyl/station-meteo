FROM alpine

# Install dependencies
RUN apt-get update
RUN apt-get install apt-utils

# Python 3.6 install
RUN apt-get install build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev
RUN apt-get install gcc
RUN apt-get install make
RUN apt-get install wget
run wget https://www.python.org/ftp/python/3.6.3/Python-3.6.3.tar.xz && tar xf Python-3.6.3.tar.xz && cd Python-3.6.3 && ./configure && make && sudo make altinstall




RUN apt-get install libsqlite3-dev
RUN apt-get install sqlite3
RUN apt-get install python3-pip
RUN python3.6 -m pip install pyephem
RUN python3.6 -m pip install sqlalchemy
RUN apt-get install python-rpi.gpio
RUN apt-get install git-core
RUN rm -rf /var/lib/apt/lists/*
RUN python3.6 -m pip install wiringpi
RUN python3.6 -m pip install apscheduler
RUN git clone https://github.com/adafruit/Adafruit_Python_MPR121.git
RUN cd Adafruit_Python_MPR121/ && python3.6 ./setup.py install

RUN python3.6 -m pip install pySerial
RUN python3.6 -m pip install smbus2
RUN python3.6 -m pip install RPi.GPIO
RUN python3.6 -m pip install paho-mqtt
RUN python3.6 -m pip install wget


# Define working directory
WORKDIR /data/shared/scripts


# Define default command
CMD ["bash"]


