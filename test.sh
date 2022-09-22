echo building docker container
docker build -f Dockerfile-rest -t jointrest:latest .

echo running docker pytest
docker run -it jointrest pytest -svv tests/modelling/geometry/test_intersections.py