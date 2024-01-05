#==========================================
#    Makefile: makefile for sl 5.1
#	Copyright 1993, 1998, 2014
#                 Toyoda Masashi
#		  (mtoyoda@acm.org)
#	Last Modified: 2014/03/31
#==========================================

CC=mips-linux-gnu-gcc

all: sl

sl: sl_abort.c sl.h
	@echo "press 'q' if you want to abort the sl program"
	@$(CC) -I/home/user/git/test/include -L /home/user/git/test/lib -static -o sl_abort sl_abort.c -lncursesw -lpthread

clean:
	rm -f sl

distclean: clean


