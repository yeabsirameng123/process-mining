import re
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
        query = "MATCH ( c1 : Class ) <-[:OBSERVED]- ( e1 : Event ) -[df:DF]-> ( e2 : Event ) -[:OBSERVED]-> ( c2 : Class ) MATCH (e1) -[:CORR] -> (n) <-[:CORR]- (e2) WHERE c1.Type = c2.Type AND n.EntityType = df.EntityType WITH n.EntityType as EType,c1,count(df) AS df_freq,c2 MERGE ( c1 ) -[rel2:DF_C {EntityType:EType}]-> ( c2 ) ON CREATE SET rel2.count=df_freq return c1, c2, rel2.count as counter LIMIT 1000"
        with self.driver.session() as session:
            result = session.run(query)
            return [(record['c1'], record['c2'], record['counter']) for record in result]

    def fetch_relation_frequency(self, relation_type):
        query = "MATCH ()-[r]->() WHERE type(r) = $relation RETURN COUNT(r) AS freq"
        with self.driver.session as session:
            result = session.run(query, relation = relation_type).single()
            relation_frequency = result['freq'] if result else 0
            return relation_frequency
        
    def fetch(self):
        query="MATCH (n:Person) RETURN n LIMIT 25"
        with self.driver.session() as session:
            result = session.run(query)
            nodes = [record['n'] for record in result]
            return nodes

        
    def create_node(self, tx, element_id, labels, properties):
        # for key, value in properties.items():
        #     properties[key] = str(value)
        # flattened_properties = {key: str(value) if not isinstance(value, (int, float, str, bool)) else value for key, value in properties.items()}
        create_node_query = (
        "CREATE (n:Class {element_id: $element_id, labels: $labels, Type: $properties.Type, ID: $properties.ID, Name: $properties.Name}) "
        "RETURN id(n) AS node_id"
        )
        result = tx.run(create_node_query, element_id=element_id, labels=labels, properties=properties)
        return result.single()["node_id"]


    def create_relationship(self, tx, id1, id2):
        create_relationship_query = "MATCH (n1:Class), (n2:Class) WHERE id(n1)=$id1 AND id(n2) =$id2 CREATE (n1)-[:RELATED_TO]->(n2)"
        tx.run(create_relationship_query, id1=id1, id2=id2)

    def parse_node_info(self,node_str):
        properties_part = node_str.split("properties=")[1].strip(">").strip()
        element_id = node_str.split("element_id=")[1].split(' ')[0].strip("'").strip("")
        labels_part = node_str.split("labels=")[1].split(' ')[0]
        return element_id, labels_part, eval(properties_part)
    
    def clear_database(self):
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
 

    def connect_and_execute_queries(self, paths_without_duplicates):
        with self.driver.session() as session:
            for subpaths in paths_without_duplicates:
                last=[]
                for i in range(len(subpaths) - 1):
                    node=str(subpaths[i])
                    current_element_id, current_labels_part, current_properties = self.parse_node_info(node)
                    node2=str(subpaths[i+1])
                    next_element_id, next_labels_part, next_properties = self.parse_node_info(node2)

                    node_id=session.write_transaction(self.create_node, current_element_id, current_labels_part, current_properties)

                    if(i>0):
                        session.write_transaction(self.create_relationship,last[0],node_id)
                        last=[]

                    other_node_id=session.write_transaction(self.create_node, next_element_id, next_labels_part, next_properties)
                    last.append(other_node_id)
                    session.write_transaction(self.create_relationship,node_id,other_node_id)
