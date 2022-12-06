image:
	docker build -t pingcadabra:latest .
run:
	docker run -it --rm -p 5050:80 -v bot:/bot/data --name PP010 pingcadabra:latest

