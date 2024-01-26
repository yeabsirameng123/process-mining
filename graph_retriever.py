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
		query = "MATCH ( c1 : Class ) <-[:OBSERVED]- ( e1 : Event ) -[df:DF]-> ( e2 : Event ) -[:OBSERVED]-> ( c2 : Class ) RETURN c1, c2"
		query = "MATCH ( c1 : Class ) <-[:OBSERVED]- ( e1 : Event ) -[df:DF]-> ( e2 : Event ) -[:OBSERVED]-> ( c2 : Class ) MATCH (e1) -[:CORR] -> (n) <-[:CORR]- (e2) WHERE c1.Type = c2.Type AND n.EntityType = df.EntityType WITH n.EntityType as EType,c1,count(df) AS df_freq,c2 MERGE ( c1 ) -[rel2:DF_C {EntityType:EType}]-> ( c2 ) ON CREATE SET rel2.count=df_freq return c1, c2, rel2.count as counter"
		with self.driver.session() as session:
			result = session.run(query)
			return [(record['c1'], record['c2'], record['counter']) for record in result]

	def fetch_relation_frequency(self, relation_type):
		query = "MATCH ()-[r]->() WHERE type(r) = $relation RETURN COUNT(r) AS freq"
		with self.driver.session as session:
			result = session.run(query, relation = relation_type).single()
			relation_frequency = result['freq'] if result else 0
			return relation_frequency
