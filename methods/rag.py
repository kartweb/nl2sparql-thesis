from SPARQLWrapper import SPARQLWrapper, JSON

class RAG:
    def __init__(self, endpoint_url="http://localhost:9999/blazegraph/sparql"):
        self.sparql = SPARQLWrapper(endpoint_url)
        self.sparql.setReturnFormat(JSON)

    def retrieve_terms(self, token):
        """Retrieve triples containing the token in subject, predicate, or object"""
        token_lower = token.lower()
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
        LIMIT 30
        """
        
        self.sparql.setQuery(query) 
        
        try:
            results = self.sparql.queryAndConvert() 
            bindings = results["results"]["bindings"]

            terms = []
            for r in bindings:
                for part in ["s","p","o"]:
                    value = r[part]["value"]
                    if token_lower in value.lower():
                        terms.append(value)
        except Exception as e:
            print(f"error: {e}")
            terms = []
        
        return terms
