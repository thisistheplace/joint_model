echo killing old docker processes
docker-compose -f docker-compose-debug.yml rm -fs

echo building docker containers
docker-compose -f docker-compose-debug.yml up --build -d