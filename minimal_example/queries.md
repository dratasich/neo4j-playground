# Minimal Example


## Preprocess

[Copy some coordinates](https://nominatim.openstreetmap.org/ui/search.html?q=london) to `nodes.csv`.
Link the nodes in `edges.csv`.

Copy files to import volume:
```bash
$ docker cp minimal_example/ neo4j-playground_neo4j_1:/var/lib/neo4j/import
```

## Load data

```cypher
// cleanup
MATCH (n)-[e]-(m) DELETE e
MATCH (n) DELETE n
MATCH (n) RETURN n LIMIT 5

// load nodes
LOAD CSV WITH HEADERS FROM 'file:///minimal_example/nodes.csv' AS row
MERGE (n:Town {
	id: row.id,
    name: row.name,
    point: point({latitude: toFloat(row.latitude), longitude: toFloat(row.longitude)})
})

// load edges
LOAD CSV WITH HEADERS FROM 'file:///minimal_example/edges.csv' AS row
MATCH (a:Town {id: row.node_from})
MATCH (b:Town {id: row.node_to})
MERGE (a)-[e:LINKS {id: row.id, type: row.form_of_way}]-(b)
	ON CREATE SET e.name = row.name
	ON MATCH SET e.name = row.name
```

## Query

```cypher
// neighbor-towns
MATCH (a {name: "Großwarasdorf"})-[e:LINKS {type: "street"}]-(b) RETURN b

// distance between two connected towns
MATCH (a {name: "Großwarasdorf"})-[e]-(b {name: "Kleinwarasdorf"}) RETURN distance(a.point,b.point)/1000 as distance_km

// towns in 7km radius
MATCH (a {name: "Großwarasdorf"})
MATCH (b)
WHERE distance(a.point, b.point) < 7000
AND a.name <> b.name
RETURN a.name, b.name, distance(a.point, b.point) AS d
```


## References

- [Spatial functions](https://neo4j.com/docs/cypher-manual/current/functions/spatial/)
