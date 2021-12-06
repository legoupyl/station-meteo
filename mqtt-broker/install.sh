docker run --restart unless-stopped -p 1883:1883 -v /data/mqtt-broker:/data/ --name mqtt-broker eclipse-mosquitto
