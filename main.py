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
ekg_query = "MATCH (e1:Event)-[:DF]->(e2:Event) RETURN e1, e2 LIMIT 1000"
ekg_edges = graph_retriever.fetch_graph(ekg_query)
ekg = create_adjacency_list(ekg_edges)

# Fetch ECKG
eckg_query = "MATCH (ec1:Event)-[:DF]->(ec2:Event) RETURN DISTINCT ec1.termName as e1, ec2.termName as e2"
eckg_edges = graph_retriever.fetch_graph(eckg_query)
eckg = create_adjacency_list(eckg_edges)

# Close the connection
graph_retriever.close()

# Now ekg and eckg contain your graphs as adjacency lists
print("EKG:", ekg)
print("ECKG:", eckg)

heuristic_miner = HeuristicMiner(ekg, eckg, frequency_threshold, significance_threshold)

