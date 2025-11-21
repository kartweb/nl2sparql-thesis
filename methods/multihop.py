from SPARQLWrapper import SPARQLWrapper, JSON
from collections import deque, defaultdict

class MultiHop:
    def __init__(self, endpoint_url="http://localhost:9999/blazegraph/sparql"):
        self.sparql = SPARQLWrapper(endpoint_url)
        self.sparql.setReturnFormat(JSON)
    
    def retrieve_triples_for_query(self):
        query = """
        SELECT ?s ?p ?o
        WHERE {
        GRAPH <https://w3id.org/CMEO/graph/studies_metadata> {
            ?s ?p ?o .
        }
        }
        LIMIT 50000
        """
        self.sparql.setQuery(query)
        results = self.sparql.queryAndConvert()
        triples = [(r["s"]["value"], r["p"]["value"], r["o"]["value"])
                for r in results["results"]["bindings"]]
        return triples

    from collections import deque, defaultdict

    def find_path(self, triples, start, end):
        graph = defaultdict(list)

        for s,p,o in triples:
            graph[s].append((p,o))

        queue = deque([(start, [])])
        visited = set([start])

        while queue:
            node, path = queue.popleft()

            if node == end:
                return path

            for (p, o) in graph[node]:
                if o not in visited:
                    visited.add(o)
                    queue.append((o, path + [(node, p, o)]))

        return None   # no path

    def retrieve_n_hops(self, start_uri, end_literal):
        triples = self.retrieve_triples_for_query()
        return self.find_path(triples, start_uri, end_literal)

    def find_instances_of_type(self, class_uri):
        query = f"""
        SELECT ?s
        WHERE {{
        GRAPH <https://w3id.org/CMEO/graph/studies_metadata> {{
            ?s a <{class_uri}> .
        }}
        }}
        """
        self.sparql.setQuery(query)
        results = self.sparql.queryAndConvert()
        return [b["s"]["value"] for b in results["results"]["bindings"]]
    

if __name__ == "__main__":
    mh = MultiHop()
    start = mh.find_instances_of_type("http://purl.obolibrary.org/obo/obi.owl/protocol")
    end = mh.find_instances_of_type("https://w3id.org/CMEO/data_use_permission_assignment")
    print("Start: " + start[16])
    print("End: " + end[1])

    

                    