mkdir /data/mqtt-broker
cp mosquitto.conf /data/mqtt-broker/
docker run --restart unless-stopped -p 1883:1883 -v /data/mqtt-broker:/mosquitto/config --name mqtt-broker eclipse-mosquitto
