CC = gcc
CFLAGS = -Wall -Wextra -std=c99 -fsanitize=address -fno-omit-frame-pointer -g

TARGETS = SlayyQueeeen

all: $(TARGETS)

SlayyQueeeen: SlayyQueeeen.c
	$(CC) $(CFLAGS) -o SlayyQueeeen SlayyQueeeen.c

clean:
	rm -f $(TARGETS)
