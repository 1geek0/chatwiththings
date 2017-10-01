
all:	chatting-sensors.tgz

chatting-sensors.tgz:	
	rm -f chatting-sensors.tgz
	tar czf chatting-sensors.tgz Makefile *.py *.json chatsenselib/*.py

wc:
	wc chatsenselib/*.py
