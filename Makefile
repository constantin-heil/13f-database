.PHONY: up down logdelete clean

up:
	docker compose up --build

down:
	docker compose down --volumes

logdelete:
	rm logpath/*

clean: down logdelete
