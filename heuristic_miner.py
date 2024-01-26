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
		total_count = 0
		path_count = 0
		for edge in self.ekg:
			if edge[0] == start:
				total_count += 1
				if edge == path:
					path_count += 1
		
		if total_count > 0:
			return path_count / total_count
		else:
			return 0

	def expand_and_check_maximal_path(self, path):
		is_maximal = True
		for edge in self.eckg:
			if edge[0] == path[-1][1]:
				new_path = path
				new_path.append(edge)
				absolute_frequency = edge[2]
				relative_frequency = self.calculate_relative_frequency(new_path, new_path[0])
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
	