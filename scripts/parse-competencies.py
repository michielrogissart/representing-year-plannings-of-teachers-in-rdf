from SPARQLWrapper import SPARQLWrapper

resultString = ""

sparql = SPARQLWrapper("http://localhost:3030/doelen/")


def run_query(sparqlFile):
    query = ""
    with open(sparqlFile, "r") as file:
        query = ' '.join(file.readlines())
    sparql.setQuery(query)
    return sparql.queryAndConvert()

def write_result(data, target):
    f = open(target, 'w', encoding="utf-8")
    f.write(data.serialize(format="turtle"))
    f.close()

## Make educational competencies
doelen = run_query('../sparql/construct-doelen.sparql')
write_result(doelen, '../rdf-data/comp.ttl')

## Make curricula
curricula = run_query('../sparql/construct-curricula.sparql')
write_result(curricula, '../rdf-data/domain.ttl')

# ## Link diplomas with competencies
links = run_query('../sparql/construct-creds.sparql')
write_result(links, "../rdf-data/cred.ttl")