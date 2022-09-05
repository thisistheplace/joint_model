echo building docker container
docker build -t jointbuilder:latest .

echo running docker pytest
docker run -it jointbuilder pytest -svv