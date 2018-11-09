up:
	sh ./bin/up.sh --build

kill:
	sh ./bin/kill.sh

init:
	sh ./bin/install.sh

component:
	docker exec -ti dev_angular "ng generate component $(name)"
