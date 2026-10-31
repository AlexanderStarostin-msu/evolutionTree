#!usr/bin/env python

import pandas as pd
from collections import defaultdict
from anytree import Node, RenderTree

df = pd.read_csv("species.csv")

children = defaultdict(list)

for _, row in df.iterrows():
    parent = row["parent_id"]
    if pd.notna(parent):
        children[int(parent)].append(int(row["id"]))

nodes = {
    int(r["id"]): r.to_dict()
    for _, r in df.iterrows()
}

def icon(node):
    if node["status"] == "alive":
        return "🟢"

    reason = str(node["extinction"])

    if reason == "homo":
        return "🔴"

    if reason == "asteroid":
        return "☄️"

    if reason == "climate":
        return "🌍"

    return "⚫"


def print_tree(node_id, prefix="", is_last=True):

    n = nodes[node_id]

    mark = icon(n)
    years = f"[{n['start_mya']} .. {n['end_mya']}]"

    if prefix == "":
        print(f"{mark} {n['name']} {years}")
    else:
        connector = "└── " if is_last else "├── "
        print(f"{prefix}{connector}{mark} {n['name']} {years}")

    kids = children[node_id]

    for i, child in enumerate(kids):

        last_child = i == len(kids) - 1

        child_prefix = (
            prefix + "    "
            if is_last
            else prefix + "│   "
        )

        print_tree(
            child,
            child_prefix,
            last_child
        )

roots = [
    nid
    for nid in nodes
    if pd.isna(nodes[nid]["parent_id"])
]

for r in roots:
    print_tree(r)
