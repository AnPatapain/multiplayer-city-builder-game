CC=gcc
CFLAGS=-Wall
EXEC=client_c
EXECPATH=network_system/
SRCDIR=network_system/network_layer/*.c network_system/system_layer/*.c


all: $(EXEC)

$(EXEC):
	$(CC) -o $(EXECPATH)$(EXEC) $(SRCDIR) $(CFLAG)