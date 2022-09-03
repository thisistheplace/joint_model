echo building docker containers
docker build -t jointbuilder:latest .

echo running docker pytest
docker run -it jointbuilder pytest