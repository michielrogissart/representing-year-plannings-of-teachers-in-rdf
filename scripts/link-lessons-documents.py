from rdflib import Graph, Literal, Namespace, BNode
import random

# Define namespaces
baseNs = Namespace("http://myontology.com/")
RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
SCHEMA = Namespace("https://schema.org/")
MYONT = Namespace(baseNs['myont/'])
PHASE = Namespace(baseNs['lesfasen/'])
COURSEMATERIAL = Namespace(baseNs['cursusmateriaal/'])
BIBO = Namespace('http://purl.org/ontology/bibo/')
DCTERMS = Namespace('http://purl.org/dc/terms/')
CHAPTERS = Namespace(baseNs['hoofdstukken/'])
COMPETENCIES = Namespace("http://ilearn.ilabt.imec.be/vocab/onddoel/")
EXERCISES = Namespace(baseNs['oefeningen/'])

inputGraph = Graph()
inputGraph.parse('../rdf-data/real-data/coursematerials.ttl')
inputGraph.parse('../rdf-data/real-data/chapters.ttl')
inputGraph.parse('../rdf-data/real-data/booksections.ttl')
inputGraph.parse('../rdf-data/generated-data/generated-phases.ttl')
inputGraph.parse('../rdf-data/generated-data/generated-lessons.ttl')
inputGraph.parse('../rdf-data/generated-data/generated-yearplan.ttl')
inputGraph.parse('../rdf-data/real-data/exercises.ttl')

phaseGraph = Graph()
phaseGraph.parse('../rdf-data/generated-data/generated-phases.ttl')
phaseGraph.bind('bibo', BIBO)
phaseGraph.bind('dcterms', DCTERMS)
phaseGraph.bind('chapters', CHAPTERS)
phaseGraph.bind('coursematerial', COURSEMATERIAL)
phaseGraph.bind('comp', COMPETENCIES)
phaseGraph.bind('exercise', EXERCISES)


books = [COURSEMATERIAL['teacher-material-stochastiek'], COURSEMATERIAL['publisher-material-kansrekenen']]
maxPages = [inputGraph.value(b, BIBO['numPages'], None).toPython() for b in books]
phases = [s for s, _, _ in inputGraph.triples((None, RDF['type'], MYONT['LessonPhase']))]
exercises = [s for s, _, _ in inputGraph.triples((None, RDF['type'], MYONT['EducationalExercise']))]

def getChapterOfPage(page, book):
    query = ""
    with open('../sparql/get-chapter-from-book-and-page.sparql', 'r') as file:
        query = ' '.join(file.readlines())
    return inputGraph.query(query, initBindings={'page': Literal(page), 'material': book})

for p in phases:
    # Add random exercises
    numExercises = random.randint(0,3)
    for _ in range(numExercises):
            phaseGraph.add((p, MYONT['hasLearningResource'], random.choice(exercises)))
    
    # Add random excerpts from books
    for i, book in enumerate(books):
        numP = maxPages[i]
        startPage = random.randint(0, numP)
        chapter = [r.chapter for r in getChapterOfPage(startPage, book)]
        if len(chapter) > 0:
            chapter = chapter[0]
            maxPage = inputGraph.value(chapter, BIBO['pageEnd'], None)
            endPage = random.randint(startPage, maxPage.toPython())

            excerptNode = BNode()
            phaseGraph.add((p, MYONT['hasLearningResource'], excerptNode))
            phaseGraph.add((excerptNode, RDF['type'], BIBO['Excerpt']))
            phaseGraph.add((excerptNode, RDF['type'], SCHEMA['LearningResource']))
            phaseGraph.add((excerptNode, DCTERMS['isPartOf'], book))
            phaseGraph.add((excerptNode, BIBO['pageStart'], Literal(startPage)))
            phaseGraph.add((excerptNode, BIBO['pageEnd'], Literal(endPage)))


phaseGraph.serialize('../rdf-data/generated-data/generated-phases-with-excerpts.ttl', format='turtle')

