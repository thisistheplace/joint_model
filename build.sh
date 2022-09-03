echo building docker containers
docker build -t thisistheplace/gmsh:latest -f Dockerfile-gmsh .
docker build -t jointbuilder:latest -f Dockerfile .

echo running docker pytest
docker run -it jointbuilder pytest