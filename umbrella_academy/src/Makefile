all: umbrella_academy-O3 umbrella_academy-O2 umbrella_academy-O1 umbrella_academy-O0

%-O3: %.c
	gcc -o $@ -Wall -O3 $< -lm
	strip -s $@

%-O2: %.c
	gcc -o $@ -Wall -O2 $< -lm
	strip -s $@

%-O1: %.c
	gcc -o $@ -Wall -O1 $< -lm
	strip -s $@

%-O0: %.c
	gcc -o $@ -Wall -O1 $< -lm
	strip -s $@
