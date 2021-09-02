# Macros
CC = gcc

# Dependency rules for non-file targets

all: myish
clobber: clean
	rm -f *~ \#*\# core
clean:
	rm -f *.o

# Dependency rules for file targets
myish: main.o commands.o dfa.o dynarray.o
	$(CC)   main.o commands.o dfa.o dynarray.o -D_GNU_SOURCE -D_BSD_SOURCE  -o myish

main.o: main.c commands.h dfa.h dynarray.h
	$(CC)  -c main.c

commands.o: commands.c commands.h dfa.h dynarray.h
	$(CC)  -c -D_BSD_SOURCE commands.c

dfa.o:	dfa.c dfa.h dynarray.h
	$(CC)  -c dfa.c

dynarray.o: dynarray.c dynarray.h
	$(CC)  -c dynarray.c
