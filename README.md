# neo4j


## Usage with docker

- `docker-compose up`
- Browse `localhost:7474`
- Choose `bolt://` protocol and connect

Data is persisted in the docker area, check path with
`docker inspect neo4j-playground_neo4j_1 | jq '.[].Mounts'`.


## References

- [neo4j official docker images](https://hub.docker.com/_/neo4j)
- [docker named volumes](https://docs.docker.com/storage/volumes/)
