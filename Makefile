
deps:
	sudo pip3 install pyusb
	sudo pip3 install adafruit-circuitpython-dht
	sudo pip3 install Adafruit_DHT
	sudo pip3 install si1145
	sudo pip3 install Adafruit_GPIO
	sudo pip3 install adafruit-circuitpython-seesaw
	sudo pip3 install adafruit-blinka
	#sudo pip3 install prometheus_client
	sudo pip3 install paho-mqtt
	sudo apt install -y mosquitto mosquitto-clients
	sudo systemctl enable mosquitto.service

services:
	sudo mv services/* /etc/systemd/system/.
	# sudo systemctl enable hass
	sudo systemctl enable sensors
	sudo systemctl enable relay

update-python:
	sudo apt-get install -y build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libffi-dev
	version=3.8.5
	wget https://www.python.org/ftp/python/$version/Python-$version.tgz
	tar zxf Python-$version.tgz
	cd Python-$version
	./configure --enable-optimizations
	make -j4
	sudo make altinstall
	update-alternatives --install /usr/bin/python python /usr/local/bin/python3.8 1
	/usr/bin/python -m pip install --upgrade pip
	curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

install-node:
	bash <(curl -sL https://raw.githubusercontent.com/node-red/linux-installers/master/deb/update-nodejs-and-nodered)
	npm i node-red-dashboard
	sudo systemctl enable nodered.service