from graph_retriever import GraphRetriever
from heuristic_miner import HeuristicMiner

uri = "neo4j://localhost:7687"  # Replace with your URI
username = "neo4j"              # Replace with your username
password = "qwerqwer"           # Replace with your password
frequency_threshold = 50
significance_threshold = 0.8


def create_adjacency_list(edges):
	graph = {}
	for (start, end) in edges:
		if start not in graph:
			graph[start] = []
		graph[start].append(end)
	return graph

# Initialize GraphRetriever
graph_retriever = GraphRetriever(uri, username, password)

# Fetch EKG
ekg_edges = graph_retriever.fetch_ekg_graph()
ekg = create_adjacency_list(ekg_edges)

# Fetch ECKG
eckg_edges = graph_retriever.fetch_eckg_graph()
eckg = create_adjacency_list(eckg_edges)

# Close the connection

# Now ekg and eckg contain your graphs as adjacency lists
print("EKG:", ekg)
print("ECKG:", eckg)

heuristic_miner = HeuristicMiner(ekg, eckg, frequency_threshold, significance_threshold, graph_retriever)

significance_paths = heuristic_miner.find_maximal_significant_paths()

graph_retriever.close()
