# Example: Gleisnetz


## Preprocess

Austrias traffic network from GIP comes as [gpkg](https://www.geopackage.org/)
that is an sqlite file.
On Linux the CLI tool `sqlite3` can list tables and provide other insights to the database.
However, the routing export already joins the nodes and relationships into `Node.txt` and `Link.txt`, respectively.

From `LUT_SUBNET_OGD_csv.csv`:
|   ID | NAME                           |
| 1200 | Land BGLD: Bahnnetz Burgenland |
| 1150 | Land BGLD: Radwege Burgenland  |

Change `*.txt` to csvs:
```bash
# routingexport txt to csv
$ cd A_routingexport_ogd_split
$ grep -E "^atr|rec" Link.txt > edges.csv
$ grep -E "^atr|rec" Node.txt > nodes.csv
$ cd ..
# extract railways and cycle paths in Burgenland
$ grep -E "^atr|^rec.*;1200;.*" A_routingexport_ogd_split/edges.csv > bgld/bgld_bahnnetz_edges.csv
$ grep -E "^atr|^rec.*;1150;.*" A_routingexport_ogd_split/edges.csv > bgld/bgld_radwege_edges.csv
# filter nodes based on existing relationships
$ ./preprocess.py -o bgld_bahnnetz A_routingexport_ogd_split/nodes.csv bgld/bgld_bahnnetz_edges.csv
$ ./preprocess.py -o bgld_radwege A_routingexport_ogd_split/nodes.csv bgld/bgld_radwege_edges.csv
```

[Copy](https://github.com/moby/moby/issues/25245) the files to the docker volume.


## Load data

```cypher
// cleanup
MATCH (n) DELETE n
MATCH (n) RETURN n LIMIT 5

// load nodes
LOAD CSV WITH HEADERS FROM 'file:///bgld_bahnnetz/nodes.csv' AS row
MERGE (c:RailwayNode {
	id: row.id,
    point: point({latitude: toFloat(row.latitude), longitude: toFloat(row.longitude), height: toFloat(row.height)})
})

// load edges
LOAD CSV WITH HEADERS FROM 'file:///bgld_bahnnetz/edges.csv' AS row
MATCH (a:RailwayNode {id: row.node_from})
MATCH (b:RailwayNode {id: row.node_to})
MERGE (a)-[e:LINKS {id: row.id, subnet_id: row.subnet_id}]-(b)
	ON CREATE SET e.name = row.name, e.form_of_way = row.form_of_way, e.width = row.width, e.level = row.level, e.baustatus = row.baustatus
	ON MATCH SET e.name = row.name, e.form_of_way = row.form_of_way, e.width = row.width, e.level = row.level, e.baustatus = row.baustatus
```

## Query


## References

- [GIP data - Netzkarte Österreich](https://www.data.gv.at/katalog/dataset/3fefc838-791d-4dde-975b-a4131a54e7c5)
- [GIP data description](https://www.gip.gv.at/assets/downloads/2012_dokumentation_gipat_ogd.pdf)
- [Relational to neo4j guide with example](https://neo4j.com/developer/guide-importing-data-and-etl/)
- [Load csv to neo4j](https://neo4j.com/docs/cypher-manual/current/clauses/load-csv/)
- [Working With Spatial Data In Neo4j GraphQL In The Cloud](https://blog.grandstack.io/working-with-spatial-data-in-neo4j-graphql-in-the-cloud-eee2bf1afad?gi=3f8846e4302b)
- [How to transform a REST service to a graph service](https://blog.grandstack.io/how-to-transform-a-rest-service-to-a-graph-service-d2ae8c5bd10d)
- [Import DB with neo4j ETL tool](https://medium.com/neo4j/neo4j-etl-tool-1-3-1-release-white-winter-2fc3c794d6a5)


## Appendix

Export [sqlite to csv](https://www.sqlitetutorial.net/sqlite-tutorial/sqlite-export-csv/):
```bash
$ sqlite3 gip_network_ogd.gpkg
SQLite version 3.31.1 2020-01-27 19:55:54
Enter ".help" for usage hints.
sqlite> .headers on
sqlite> .mode csv
sqlite> .output bgld_bahnnetz.csv
sqlite> select LINK_ID,NAME1,FROM_NODE,TO_NODE from GIP_LINKNETZ_OGD where SUBNET_ID=1200;
sqlite> .output bgld_radwege.csv
sqlite> select LINK_ID,NAME1,FROM_NODE,TO_NODE from GIP_LINKNETZ_OGD where SUBNET_ID=1150;
sqlite> .quit
```
