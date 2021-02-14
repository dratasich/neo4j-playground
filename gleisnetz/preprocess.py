#!/bin/env python3

# %% imports
import argparse
import os
import numpy as np
import pandas as pd

# %% parse arguments
parser = argparse.ArgumentParser(description="Process some integers.")
parser.add_argument("nodes", type=argparse.FileType("r"), help="CSV of nodes.")
parser.add_argument("edges", type=argparse.FileType("r"), help="CSV of edges.")
parser.add_argument("-o", "--output-dir", default="data", help="Output directory CSVs.")
args = parser.parse_args()

# %% read nodes and edges from csv
edges = pd.read_csv(args.edges, sep=";", na_values=[-1.0])
nodes = pd.read_csv(args.nodes, sep=";", na_values=[-1.0])
#edges = pd.read_csv("bgld/bgld_radwege_edges.csv", sep=";", na_values=[-1.0])
#nodes = pd.read_csv("A_routingexport_ogd_split/nodes.csv", sep=";", na_values=[-1.0])

# %% filter nodes based on nodes listed in edges
edge_nodes = edges.FROM_NODE.append(edges.TO_NODE).drop_duplicates()
nodes = nodes[nodes.NODE_ID.isin(edge_nodes)]

# %% filter columns
nodes = nodes[["NODE_ID", "X", "Y", "Z"]]
edges = edges[["LINK_ID", "NAME1", "FROM_NODE", "TO_NODE", "FORMOFWAY", "WIDTH", "LEVEL", "BAUSTATUS", "SUBNET_ID"]]

# %% rename columns
nodes.rename(columns={
    "NODE_ID": "id",
    "X": "longitude",
    "Y": "latitude",
    "Z": "height",
}, inplace=True)
edges.rename(columns={
    "LINK_ID": "id",
    "NAME1": "name",
    "FROM_NODE": "node_from",
    "TO_NODE": "node_to",
    "FORMOFWAY": "form_of_way",
    "WIDTH": "width",
    "LEVEL": "level",
    "BAUSTATUS": "baustatus",
    "SUBNET_ID": "subnet_id",
}, inplace=True)

# %% export back to csv file, with comma as separator
os.makedirs(args.output_dir, exist_ok=True)
nodes.to_csv(f"{args.output_dir}/nodes.csv", index=False)
edges.to_csv(f"{args.output_dir}/edges.csv", index=False)
