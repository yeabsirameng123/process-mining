from graph_retriever import GraphRetriever
from heuristic_miner import HeuristicMiner

uri = "bolt://localhost:7687"  # Replace with your URI
username = "neo4j"              # Replace with your username
password = "12345678"           # Replace with your password
frequency_threshold = 250
significance_threshold = 0.2



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

# Initialize GraphRetriever
graph_retriever = GraphRetriever(uri, username, password)

print("Fetching EKG...")

# Fetch EKG
ekg_edges = graph_retriever.fetch_ekg_graph()


ekg = create_adjacency_list(ekg_edges)

print("Finished fetching EKG")
print("Fetching ECKG...")

# Fetch ECKG
eckg_edges = graph_retriever.fetch_eckg_graph()
eckg = create_eckg_adjacency_list(eckg_edges)
print(eckg_edges)
eckg =eckg_edges

#print("Finished fetching ECKG")



# Now ekg and eckg contain your graphs as adjacency lists
#print("EKG:", ekg)
print("ECKG:", eckg)

print("Creating HeuristicMiner...")

heuristic_miner = HeuristicMiner(ekg, eckg, frequency_threshold, significance_threshold, graph_retriever)

print("Finished creating HeuristicMiner")
print("Computing significant paths...")

significance_paths = heuristic_miner.find_maximal_significant_paths()

print(significance_paths)

print("Finished computing significant paths")
print("Found " + str(len(significance_paths)) + " paths")

print("Closing database...")

graph_retriever.close()

print("Finished closing database")
