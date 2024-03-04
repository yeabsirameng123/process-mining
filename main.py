from graph_retriever import GraphRetriever
from heuristic_miner import HeuristicMiner
import time

uri = "neo4j://localhost:7687"  # Replace with your URI
username = "neo4j"              # Replace with your username
password = "qwerqwer"           # Replace with your password
frequency_threshold = 5
significance_threshold = 0.01


def create_adjacency_list(edges):
	graph = {}
	for (start, end) in edges:
		id = start.get('Activity')
		if id not in graph:
			graph[id] = [start]
		graph[id].append(end)
	return graph


def create_eckg_adjacency_list(edges):
	graph = {}
	for (start, end, count) in edges:
		if start not in graph:
			graph[start] = []
		graph[start].append((end, count))
	return graph

start_time = time.time()

graph_retriever = GraphRetriever(uri, username, password)

print("Fetching EKG...")

# Fetch EKG
ekg_edges = graph_retriever.fetch_ekg_graph()
ekg = create_adjacency_list(ekg_edges)

print("Finished fetching EKG")
ekg_time = time.time()
print("Fetching ECKG...")

# Fetch ECKG
eckg_edges = graph_retriever.fetch_eckg_graph()
#eckg = create_eckg_adjacency_list(eckg_edges)
eckg =eckg_edges

print("Finished fetching ECKG")
eckg_time = time.time()



# Now ekg and eckg contain your graphs as adjacency lists
#print("EKG:", ekg)
#print("ECKG:", eckg)

print("Creating HeuristicMiner...")

heuristic_miner = HeuristicMiner(ekg, eckg, frequency_threshold, significance_threshold, graph_retriever)

print("Finished creating HeuristicMiner")
print("Computing significant paths...")

significance_paths = heuristic_miner.find_maximal_significant_paths()

print(significance_paths)

print("Finished computing significant paths")
print("Found " + str(len(significance_paths)) + " paths")

print("Closing database...")
end_time = time.time()

graph_retriever.close()

paths_without_duplicates = [i for n, i in enumerate(significance_paths) if i not in significance_paths[:n]]

file_path = "output.txt"

# Open the file in write mode
with open(file_path, 'w') as f:
    # Iterate over each sublist in the array
    for path in paths_without_duplicates:
        # Convert each element to a string and join them with commas
        line = ','.join(map(str, path))
        # Write the line to the file
        f.write(line + '\n')

print("Finished closing database")
print("Fetching ekg: " + str((ekg_time - start_time)))
print("Fetching eckg: " + str((eckg_time - ekg_time)))
print("Calculating: " + str((end_time - eckg_time)))
print("Total: " + str((end_time - start_time)))
