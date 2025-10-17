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
    
    def retrieve_n_hops(self, entity_uri):

        if not entity_uri.startswith("<"):
            entity_uri = f"<{entity_uri}>"

        query = f"""
        PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT DISTINCT
        ?pathStart
        ?p1 ?mid1
        ?p2 ?mid2
        ?p3 ?mid3
        ?p4 ?mid4
        ?p5 ?mid5
        ?p6 ?mid6
        ?p7
        ?end
        ?hops
        WHERE {{
        GRAPH <https://w3id.org/CDIO/graph/studies> {{
            # Bind the given entity (e.g., diabetes) as the fixed end target
            BIND({entity_uri} AS ?end)

            {{
            # 1 hop
            ?pathStart ?p1 ?end .
            BIND(1 AS ?hops)
            }}
            UNION
            {{
            # 2 hops
            ?pathStart ?p1 ?mid1 .
            ?mid1 ?p2 ?end .
            BIND(2 AS ?hops)
            }}
            UNION
            {{
            # 3 hops
            ?pathStart ?p1 ?mid1 .
            ?mid1 ?p2 ?mid2 .
            ?mid2 ?p3 ?end .
            BIND(3 AS ?hops)
            }}
            UNION
            {{
            # 4 hops
            ?pathStart ?p1 ?mid1 .
            ?mid1 ?p2 ?mid2 .
            ?mid2 ?p3 ?mid3 .
            ?mid3 ?p4 ?end .
            BIND(4 AS ?hops)
            }}
            UNION
            {{
            # 5 hops
            ?pathStart ?p1 ?mid1 .
            ?mid1 ?p2 ?mid2 .
            ?mid2 ?p3 ?mid3 .
            ?mid3 ?p4 ?mid4 .
            ?mid4 ?p5 ?end .
            BIND(5 AS ?hops)
            }}
            UNION
            {{
            # 6 hops
            ?pathStart ?p1 ?mid1 .
            ?mid1 ?p2 ?mid2 .
            ?mid2 ?p3 ?mid3 .
            ?mid3 ?p4 ?mid4 .
            ?mid4 ?p5 ?mid5 .
            ?mid5 ?p6 ?end .
            BIND(6 AS ?hops)
            }}
            UNION
            {{
            # 7 hops
            ?pathStart ?p1 ?mid1 .
            ?mid1 ?p2 ?mid2 .
            ?mid2 ?p3 ?mid3 .
            ?mid3 ?p4 ?mid4 .
            ?mid4 ?p5 ?mid5 .
            ?mid5 ?p6 ?mid6 .
            ?mid6 ?p7 ?end .
            BIND(7 AS ?hops)
            }}

            # Prevent cycles
            FILTER(
            !BOUND(?mid1) || (
                ?pathStart != ?mid1 &&
                (!BOUND(?mid2) || (?mid1 != ?mid2 && ?pathStart != ?mid2)) &&
                (!BOUND(?mid3) || (?mid2 != ?mid3 && ?mid1 != ?mid3 && ?pathStart != ?mid3)) &&
                (!BOUND(?mid4) || (?mid3 != ?mid4 && ?mid2 != ?mid4 && ?mid1 != ?mid4 && ?pathStart != ?mid4)) &&
                (!BOUND(?mid5) || (?mid4 != ?mid5 && ?mid3 != ?mid5 && ?mid2 != ?mid5 && ?mid1 != ?mid5 && ?pathStart != ?mid5)) &&
                (!BOUND(?mid6) || (?mid5 != ?mid6 && ?mid4 != ?mid6 && ?mid3 != ?mid6 && ?mid2 != ?mid6 && ?mid1 != ?mid6 && ?pathStart != ?mid6))
            )
            )
        }}
        }}
        ORDER BY DESC(?hops)
        LIMIT 1
        """


        self.sparql.setQuery(query)
        try:
            results = self.sparql.queryAndConvert()
            bindings = results["results"]["bindings"]

            triples = []
            for r in bindings:
                s = r.get("pathStart", {}).get("value", "")
                end = entity_uri.strip("<>")
                current = s

                # build clean chain
                for i in range(1, 8):
                    p = r.get(f"p{i}", {}).get("value")
                    m = r.get(f"mid{i}", {}).get("value")
                    if p and m:
                        triples.append((current, p, m))
                        current = m
                    elif p and not m:
                        triples.append((current, p, end))
                        break


            return triples
        
        except Exception as e:
            print(f"Error during sparql execution: {e}")
            triples = []
        
        return triples
                    