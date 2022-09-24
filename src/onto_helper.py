from rdflib import Graph


def get_keywords(ontology_file_path: str):
    g = Graph()
    g.parse(ontology_file_path)

    query = """
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        SELECT DISTINCT ?s_label ?o_label ?search_term_label WHERE { 
            ?s ?p ?o .
                ?s rdfs:label ?s_label .
                ?o rdfs:label ?o_label .
            OPTIONAL{
                ?search_term <http://www.semanticweb.org/falguni/ontologies/2022/8/www.custom-ontology.org#is_search_term> true .
                ?search_term rdfs:label ?search_term_label .
            }
            
        }
    """

    res = g.query(query)

    labels = set()
    search_terms = set()

    for row in res:
        if row.s_label:
            labels.add(str(row.s_label))

        if row.o_label:
            labels.add(str(row.o_label))

        if row.search_term_label:
            search_terms.add(str(row.search_term_label))

    keywords = {
        "search_terms": list(search_terms),
        "other_labels": list(labels)
    }

    return keywords
