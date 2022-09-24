echo building docker container
docker build -f Dockerfile-test -t jointrest:latest .

echo running docker pytest
docker run -it jointrest pytest -svv src