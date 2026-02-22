import pandas as pd
import networkx as nx
from pyvis.network import Network
import pickle
import os

# =====================================
# PATH CONFIGURATION (PROJECT SAFE)
# =====================================

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

DATA_PATH = os.path.join(BASE_DIR, "data", "raw", "fraud_dataset.csv")
GRAPH_PATH = os.path.join(BASE_DIR, "data", "graph", "transaction_graph.pkl")
HTML_PATH = os.path.join(BASE_DIR, "visualizations", "graph_visualization.html")

# Create folders if missing
os.makedirs(os.path.join(BASE_DIR, "data", "graph"), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "visualizations"), exist_ok=True)

# =====================================
# LOAD DATASET
# =====================================

df = pd.read_csv(DATA_PATH)

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
# SAVE GRAPH (.pkl)
# =====================================

with open(GRAPH_PATH, "wb") as f:
    pickle.dump(G, f)

print("Graph Saved at:", GRAPH_PATH)

# =====================================
# INTERACTIVE VISUALIZATION
# =====================================

# Full graph is huge → sample for visualization
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
        color = "#f39c12"   # orange (transaction)

    net.add_node(
        node,
        label=node,
        color=color,
        size=12
    )

# Add edges
for source, target in H.edges():
    net.add_edge(source, target)

# Physics settings
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

# Save visualization
net.write_html(HTML_PATH)

print("Interactive graph created at:", HTML_PATH)