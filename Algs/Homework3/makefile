CC = gcc
CFLAGS = -Wall -std=c99

all: fastinversioncount easyinversioncount gray palindromecheck

fastinversioncount: fastinversioncount.c
	$(CC) $(CFLAGS) -o fastinversioncount fastinversioncount.c

easyinversioncount: easyinversioncount.c
	$(CC) $(CFLAGS) -o easyinversioncount easyinversioncount.c

gray: gray.c
	$(CC) $(CFLAGS) -o gray gray.c

palindromecheck: palindromecheck.c
	$(CC) $(CFLAGS) -o palindromecheck palindromecheck.c

clean:
	rm -f fastinversioncount easyinversioncount gray palindromecheck
