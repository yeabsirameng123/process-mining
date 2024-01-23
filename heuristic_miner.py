class HeuristicMiner:
	def __init__(self, ekg, eckg, frequency_threshold, significance_threshold) -> None:
		self.ekg = ekg
		self.eckg = eckg
		self.frequency_threshold = frequency_threshold
		self.significance_threshold = significance_threshold

	def find_maximal_significant_paths(self):
		self.significance_paths = []
		for edge in self.eckg:
			path = [edge]

	def expand_and_check_maximal_path(self, path):
		is_maximal = True
		for edge in self.eckg:
			# TODO if extends path - I dont know how to achieve this
			...
			