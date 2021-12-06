docker build . xavfan/mqtt-db-logger
docker run --name mqtt-db-logger mqtt-db-logger bash
sudo mkdir /data
chmod 777 /data
mkdir /data/mqtt-db-logger/
cp mqtt-db-logger.py /data/mqtt-db-logger/

cd /data/mqtt-db-logger/

cat <<EOT >> mqtt_db_logger_conf.py
mqtt_brocker="####.cloudapp.net"
topic="#####"
db_srvname="#####"
db_name="#####"
db_username="###"
db_user_pwd="####"
EOT


docker run -it -v /data/mqtt-db-logger:/data --name mqtt-db-logger mqtt-db-logger bash
