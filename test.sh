echo building docker container
docker build -f Dockerfile-test -t jointbuilder:latest .

echo running docker pytest
docker run -it jointbuilder pytest