build:
	docker build -t swiftshirt-backend-2 .

run:
	docker run -p 5000:5000 swiftshirt-backend-2 

compile:
	pip install -r requirements.txt