class HeuristicMiner:
    def __init__(self, ekg, eckg, frequency_threshold, significance_threshold, graph_retriever) -> None:
        self.ekg = ekg
        self.eckg = eckg
        self.frequency_threshold = frequency_threshold
        self.significance_threshold = significance_threshold
        self.graph_retriever = graph_retriever


    def calculate_absolute_frequency(self, path):
        frequency = float('inf')
        for relation in path:
            frequency = min(frequency, self.graph_retriever.fetch_relation_frequency(relation))

        return frequency

    def calculate_relative_frequency(self, path, start):
        total_count = 1
        path_count = 0
        #tmp = self.ekg[start]
        for node_class in path:
            x=node_class[0]
            total_count=total_count*self.graph_retriever.get_events_of_class(x.get('ID'))
        id = start.get('ID')
        index = len(path)-1
        if id in self.ekg:
            for edge in self.ekg[id]:
                total_count += 1
                if edge.get('Activity') == path[index][1].get('ID'):
                    path_count += 1
            
        if total_count > 0:
            return path_count / total_count
        else:
            return 0
    

    
    
    def expand_and_check_maximal_path(self, path):
        is_maximal = True
        index = len(path)-1
        for edge in self.eckg:
            if edge[0] == path[index][1]:
                new_path = path
                new_path.append(edge)
                absolute_frequency = edge[2]
                relative_frequency = self.calculate_relative_frequency(new_path, edge[0])
                print(relative_frequency)
                if absolute_frequency >= self.frequency_threshold and relative_frequency >= self.significance_threshold:
                    is_maximal = False
                    self.expand_and_check_maximal_path(new_path)

        if is_maximal:
            self.significance_paths.append(path)

    def find_maximal_significant_paths(self):
        self.significance_paths = []
        for edge in self.eckg:
            path = [edge]
            self.expand_and_check_maximal_path(path)

        return self.significance_paths
    
