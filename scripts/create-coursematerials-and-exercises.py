from rdflib import Graph, Literal, Namespace, BNode
from rdflib.namespace import XSD
import json
import random

baseNs = Namespace("http://myontology.com/")
RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
SCHEMA = Namespace("https://schema.org/")
MYONT = Namespace(baseNs['myont/'])
COURSEMATERIAL = Namespace(baseNs['cursusmateriaal/'])
BIBO = Namespace('http://purl.org/ontology/bibo/')
DCTERMS = Namespace('http://purl.org/dc/terms/')
CHAPTERS = Namespace(baseNs['hoofdstukken/'])
EXCERPTS = Namespace(baseNs['uittreksels/'])
EXERCISES = Namespace(baseNs['oefeningen/'])
EXERCISETYPE = Namespace(baseNs['oefeningtypes/'])
COMP = Namespace('http://ilearn.ilabt.imec.be/vocab/onddoel/')

chapterGraph = Graph()
excerptGraph = Graph()
exerciseGraph = Graph()

graphs = [chapterGraph, excerptGraph, exerciseGraph]

def bindGraphs():
    for g in graphs:
        g.bind('rdf', RDF)
        g.bind('schema', SCHEMA)
        g.bind('myont', MYONT)
        g.bind('coursematerial', COURSEMATERIAL)
        g.bind('bibo', BIBO)
        g.bind('dcterms', DCTERMS)
        g.bind('chapter', CHAPTERS)
        g.bind('excerpt', EXCERPTS)
        g.bind('exercise', EXERCISES)
        g.bind('exercisetype', EXERCISETYPE)
        g.bind('comp', COMP)

def parseExercises(exerciseIndices, excerptNode, bookname, chapterIndex):
    difficulties = [Literal('Erg gemakkelijk', lang="nl"), 
                    Literal('gemakkelijk', lang="nl"),
                    Literal('gemiddeld', lang="nl"),
                    Literal('moeilijk', lang="nl"),
                    Literal('Erg moeilijk', lang="nl")]
    indices = exerciseIndices.split('-')
    startIndex = int(indices[0])
    endIndex = int(indices[1])
    for exerciseIndex in range(startIndex, endIndex+1):
        exerciseNode = EXERCISES[bookname+"-chapter"+chapterIndex+"-exercise"+str(exerciseIndex)]

        exerciseGraph.add((exerciseNode, RDF['type'], MYONT['EducationalExercise']))
        exerciseGraph.add((exerciseNode, SCHEMA['position'], Literal(int(exerciseIndex), datatype=XSD.integer)))
        exerciseGraph.add((exerciseNode, SCHEMA['isPartOf'], excerptNode))
        exerciseGraph.add((exerciseNode, SCHEMA['learningResourceType'], EXERCISETYPE['FillInQuestion']))
        exerciseGraph.add((exerciseNode, MYONT['difficulty'], random.choice(difficulties)))
        exerciseGraph.add((exerciseNode, SCHEMA['teaches'], random.choice(mathComp)))

def parseExcerpts(excerptMap, chapterIndex, booknode, bookname):
    for excerptIndex, excerptData in excerptMap.items():
        # parse excerpt data
        excerptNode = EXCERPTS[bookname+"-"+"chapter"+str(chapterIndex)+"-"+"excerpt"+str(excerptIndex)]
        excerptNameLit = Literal(excerptData["name"], lang="nl")
        pages = excerptData['pages'].split('-')
        startPage = Literal(int(pages[0]), datatype=XSD.integer)
        endPage = Literal(int(pages[1]), datatype=XSD.integer)
        nrOfCompetencies = random.randint(0, 5)
        # add excerpt data
        excerptGraph.add((excerptNode, RDF['type'], BIBO['Excerpt']))
        excerptGraph.add((excerptNode, RDF['type'], SCHEMA['LearningResource']))
        excerptGraph.add((excerptNode, BIBO['pageStart'], startPage))
        excerptGraph.add((excerptNode, BIBO['pageEnd'], endPage))
        excerptGraph.add((excerptNode, SCHEMA['name'], excerptNameLit))
        excerptGraph.add((excerptNode, DCTERMS['isPartOf'], booknode))

        for _ in range(nrOfCompetencies):
            excerptGraph.add((excerptNode, SCHEMA['teaches'], random.choice(mathComp)))

        # add exercises
        parseExercises(excerptData['exercises'], excerptNode, bookname, chapterIndex)

def parseCourseMaterialMap(map, bookname):
    booknode = COURSEMATERIAL[bookname]
    for chapterIndex, chapterData in map.items():
        # parse chapter data
        chapterNode = CHAPTERS[bookname+"-"+"chapter"+str(chapterIndex)]
        pages = chapterData["pages"].split('-')
        chapterName = Literal(chapterData['name'], lang="nl")
        startPage = Literal(pages[0], datatype=XSD.integer)
        endPage = Literal(pages[1], datatype=XSD.integer)
        chapterIndexLit = Literal(int(chapterIndex), datatype=XSD.integer)
        
        # add chapter data
        chapterGraph.add((chapterNode, RDF['type'], BIBO['Chapter']))
        chapterGraph.add((chapterNode, RDF['type'], SCHEMA['LearningResource']))
        chapterGraph.add((chapterNode, SCHEMA['name'], chapterName))
        chapterGraph.add((chapterNode, BIBO['chapter'], chapterIndexLit))
        chapterGraph.add((chapterNode, BIBO['pageStart'], startPage))
        chapterGraph.add((chapterNode, BIBO['pageEnd'], endPage))
        chapterGraph.add((chapterNode, DCTERMS['isPartOf'], booknode))

        # add excerpts
        parseExcerpts(chapterData["excerpts"], chapterIndex, booknode, bookname)


# bind graphs with prefixes
bindGraphs()

# get math competencies
compGraph = Graph()
compGraph.parse('../rdf-data/comp.ttl')
compGraph.parse('../rdf-data/domain.ttl')
compGraph.parse('../rdf-data/cred.ttl')
mathComp = []
with open('../sparql/get-math-comp-gr3-doorstroom.sparql', 'r') as file:
    compQueryResult = compGraph.query(' '.join(file.readlines()))
    mathComp.extend([row.comp for row in compQueryResult])

# parse publisher material
publisherMaterialMap = {}
with open('data/publisher-material-kansrekenen.json', 'r') as file:
    publisherMaterialMap = json.load(file)

parseCourseMaterialMap(publisherMaterialMap, "publisher-material-kansrekenen")

# parse teacher material
teacherMaterialMap = {}
with open('data/teacher-material-stochastiek.json', 'r') as file:
    teacherMaterialMap = json.load(file)

parseCourseMaterialMap(teacherMaterialMap, "teacher-material-stochastiek")

chapterGraph.serialize('../rdf-data/real-data/chapters.ttl', format='turtle')
excerptGraph.serialize('../rdf-data/real-data/bookexcerpts.ttl', format='turtle')
exerciseGraph.serialize('../rdf-data/real-data/exercises.ttl', format='turtle')
