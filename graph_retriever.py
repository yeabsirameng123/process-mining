from neo4j import GraphDatabase

class GraphRetriever:
	def __init__(self, uri, user, password):
		self.driver = GraphDatabase.driver(uri, auth=(user, password))

	def close(self):
		self.driver.close()

	def fetch_graph(self, query):
		with self.driver.session() as session:
			result = session.run(query)
			return [(record['e1'], record['e2']) for record in result]