
all:	chatting-sensors.tgz

chatting-sensors.tgz:	
	rm -f chatting-sensors.tgz
	tar czf chatting-sensors.tgz Makefile *.md *.py *.json chatsenselib/*.py

wc:
	wc chatsenselib/*.py
