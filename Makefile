all: stadyn

stadyn: stadyn.cpp obfuscate.h
	g++ -Ofast -s $< -o $@

obfuscate.h:
	curl -o obfuscate.h https://raw.githubusercontent.com/adamyaxley/Obfuscate/master/obfuscate.h

docker: Dockerfile stadyn.cpp Makefile
	docker build -t stadyn .

extract: docker
	$(eval id := $(shell docker create stadyn))
	docker cp $(id):/opt/stadyn - | tar xv stadyn
	docker rm -v $(id)

clean:
	rm -f stadyn
