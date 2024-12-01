# didactic-journey
SoftArch repo on message brokers


## How to run

### Create a virtual environment
```
$ python3 -m venv .venv
$ source .venv/bin/activate
```

### Install dependecies
```
$ pip install -r requirements.txt
```

### Run app
We have 2 implementations in the project the first one is "pipes-and-filters" which uses pipes
for services communication and a service is a process, the second is "message-brokers" where a message broker is used for services communication.

To run a pipes and filters based implementation run: 
```
$ make run-pipes-and-filters
```

To run a message broker based implementation you need to run all services
```
$ make run-message-brokers
```

## Linters and formatters

### Install dev dependecies
```
$ pip install -r requirements.dev.txt
```

### Run formatters
```
$ make format
```

### Run linters
```
$ make check
```