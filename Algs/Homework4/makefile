CC = gcc
CFLAGS = -Wall -Wextra -std=c99

TARGETS = BilbosBigBrain GaussJordanElimination

all: $(TARGETS)

BilbosBigBrain: BilbosBigBrain.c
	$(CC) $(CFLAGS) -o BilbosBigBrain BilbosBigBrain.c

GaussJordanElimination: GaussJordanElimination.c
	$(CC) $(CFLAGS) -o GaussJordanElimination GaussJordanElimination.c

clean:
	rm -f $(TARGETS)
