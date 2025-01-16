CC = gcc
CFLAGS = -Wall -Wextra -std=c99 -fsanitize=address -fno-omit-frame-pointer -g

TARGETS = Hashing Dstra

all: $(TARGETS)

Hashing: Hashing.c
	$(CC) $(CFLAGS) -o Hashing Hashing.c

Dstra: Dstra.c
	$(CC) $(CFLAGS) -o Dstra Dstra.c

clean:
	rm -f $(TARGETS)
