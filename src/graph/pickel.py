import pickle

with open("data/graph/transaction_graph.pkl", "rb") as f:
    G = pickle.load(f)

print(G)
print("Nodes:", G.number_of_nodes())
print("Edges:", G.number_of_edges())