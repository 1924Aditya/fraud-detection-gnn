import pandas as pd
import networkx as nx
from pyvis.network import Network
import pickle

# =====================================
# LOAD RAW DATASET
# =====================================

df = pd.read_csv("C:\\Users\\HP\\Desktop\\11\\ntwrk\\fraud_dataset.csv")

print("Dataset Loaded")
print("Shape:", df.shape)
print(df.head())

# =====================================
# CREATE GRAPH
# =====================================

G = nx.Graph()

for _, row in df.iterrows():

    txn = f"txn_{row['transaction_id']}"
    user = f"user_{row['user_id']}"
    merchant = f"merchant_{row['merchant_id']}"
    device = f"device_{row['device_id']}"

    # Add nodes
    G.add_node(txn, type="transaction")
    G.add_node(user, type="user")
    G.add_node(merchant, type="merchant")
    G.add_node(device, type="device")

    # Add edges
    G.add_edge(user, txn)
    G.add_edge(txn, merchant)
    G.add_edge(txn, device)

print("\nGraph Created Successfully")
print("Total Nodes:", G.number_of_nodes())
print("Total Edges:", G.number_of_edges())

# =====================================
# SAVE GRAPH
# =====================================

with open("C:\\Users\\HP\\Desktop\\11\\ntwrk\\transaction_graph.pkl", "wb") as f:
    pickle.dump(G, f)

print("Graph Saved.")

# =====================================
# INTERACTIVE VISUALIZATION
# =====================================

# IMPORTANT:
# Full graph is huge → take sample
sample_nodes = list(G.nodes())[:300]
H = G.subgraph(sample_nodes)

net = Network(
    height="750px",
    width="100%",
    bgcolor="#111111",
    font_color="white"
)

# Add nodes with colors
for node, data in H.nodes(data=True):

    node_type = data["type"]

    if node_type == "user":
        color = "#3498db"   # blue
    elif node_type == "merchant":
        color = "#e74c3c"   # red
    elif node_type == "device":
        color = "#2ecc71"   # green
    else:
        color = "#f39c12"   # orange

    net.add_node(
        node,
        label=node,
        color=color,
        size=12
    )

# Add edges
for source, target in H.edges():
    net.add_edge(source, target)

# Physics settings (dynamic movement)
net.set_options("""
var options = {
  "physics": {
    "barnesHut": {
      "gravitationalConstant": -12000,
      "springLength": 120
    },
    "minVelocity": 0.75
  }
}
""")

# Save interactive graph
net.write_html("graph_visualization.html")

print("Interactive graph created successfully.")