from neo4j import GraphDatabase

class GraphRetriever:
	def __init__(self, uri, user, password):
		self.driver = GraphDatabase.driver(uri, auth=(user, password))

	def close(self):
		self.driver.close()

	def fetch_ekg_graph(self):
		query = "MATCH (e1:Event)-[:DF]->(e2:Event) RETURN e1, e2 LIMIT 1000"
		with self.driver.session() as session:
			result = session.run(query)
			return [(record['e1'], record['e2']) for record in result]

	def fetch_eckg_graph(self):
		# query = "MATCH (ec1:Event)-[:DF]->(ec2:Event) RETURN DISTINCT ec1.termName as e1, ec2.termName as e2"
		query = "MATCH ( c1 : Class ) <-[:OBSERVED]- ( e1 : Event ) -[df:DF]-> ( e2 : Event ) -[:OBSERVED]-> ( c2 : Class ) RETURN c1, c2 LIMIT 1000"
		with self.driver.session() as session:
			result = session.run(query)
			return [(record['c1'], record['c2']) for record in result]

	def fetch_relation_frequency(self, relation):
		query = "MATCH ()-[r]->() WHERE type(r) = $relation RETURN COUNT(r) AS freq"
		with self.driver.session as session:
			result = session.run(query, relation = relation).single()
			relation_frequency = result['freq'] if result else 0
			return relation_frequency
