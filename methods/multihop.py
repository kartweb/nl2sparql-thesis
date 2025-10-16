from SPARQLWrapper import SPARQLWrapper, JSON

class MultiHop:
    def __init__(self, endpoint_url="http://localhost:9999/blazegraph/sparql"):
        self.sparql = SPARQLWrapper(endpoint_url)
        self.sparql.setReturnFormat(JSON)

    def retrieve_one_hop(self, entity_uri):
        
        # Ensure entity URI is enclosed in <...>
        if not entity_uri.startswith("<"):
            entity_uri = f"<{entity_uri}>"

        query = f"""
        PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT DISTINCT ?s ?p ?o
        WHERE {{
            GRAPH <https://w3id.org/CDIO/graph/studies> {{
                {{
                    {entity_uri} ?p ?o .
                    BIND({entity_uri} AS ?s)
                }}
                UNION
                {{
                    ?s ?p {entity_uri} .
                    BIND({entity_uri} AS ?o)
                }}
            }}
        }}
        LIMIT 30
        """

        self.sparql.setQuery(query)
        try:
            results = self.sparql.queryAndConvert()
            bindings = results["results"]["bindings"]

            triples = []
            for r in bindings:
                s = r["s"]["value"]
                p = r["p"]["value"]
                o = r["o"]["value"]
                triples.append((s, p, o))
        
        except Exception as e:
            print(f"error during sparql execution: {e}")
            triples = []

        return triples
                