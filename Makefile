run:
	docker build -t swiftshirt-backend-2 .
	docker run -p 5000:5000 swiftshirt-backend-2
