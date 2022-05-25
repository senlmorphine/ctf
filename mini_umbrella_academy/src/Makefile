all: mini_umbrella_academy-O3 mini_umbrella_academy-O2 mini_umbrella_academy-O1

%-O3: %.c
	gcc -o $@ -Wall -O3 $< -lm
	strip -s $@

%-O2: %.c
	gcc -o $@ -Wall -O2 $< -lm
	strip -s $@

%-O1: %.c
	gcc -o $@ -Wall -O1 $< -lm
	strip -s $@
