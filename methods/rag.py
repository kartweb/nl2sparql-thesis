#retrieve all triples matcing with tokens
#retrieve all paths connecting tokens
#using blazegraph natively over pythong networkx and rdflib for scalability 

from SPARQLWrapper import SPARQLWrapper, JSON

class RAG:
    def __init__(self, endpoint_url="http://localhost:9999/blazegraph/"):
        self.sparql = SPARQLWrapper(endpoint_url)
        self.sparql.setReturnFormat(JSON)

    def retrieve_triples(self, token):
        """Retrieve triples containing the token in subject, predicate, or object"""
        #double {{ to escape f-string }}
        query = f"""
        SELECT ?s ?p ?o WHERE {{ 
            GRAPH <https://w3id.org/CDIO/graph/studies> {{
                ?s ?p ?o .
                FILTER(
                    CONTAINS( LCASE( STR(?s) ), LCASE("{token}")) ||
                    CONTAINS( LCASE( STR(?p) ), LCASE("{token}")) ||
                    CONTAINS( LCASE( STR(?o) ), LCASE("{token}"))
                )
            }}
        }} 
        """
        
        self.sparql.setQuery(query) #set the sparql query text
        
        try:
            results = self.sparql.queryAndConvert() #execute the query and convert the results to JSON
            bindings = results["results"]["bindings"]
            triples = [
                (r["s"]["value"], r["p"]["value"], r["o"]["value"]) 
                for r in bindings
            ]
        except Exception as e:
            print(e)
            triples = []
        
        return triples
