check:
	mypy --show-error-codes .
	
format:
	ruff check --fix
	isort .

run-pipes-and-filters:
	cd pipes-and-filters && uvicorn main:app

run-message-brockers:
	docker run -d \
		--rm \
		--name rabbitmq\
		-p 5672:5672 \
		-p 15672:15672 \
		rabbitmq:4.0-management

	@echo "Waiting 5 seconds the message broker is started"
	sleep 5

	@echo "Running filter service"
	cd message-brokers && python filter/main.py &
	
	@echo "Running publish service"
	cd message-brokers && python publish/main.py &

	@echo "Running rest service"
	cd message-brokers && uvicorn rest.main:app &

	@echo "Running filter service"
	cd message-brokers && python screaming/main.py
