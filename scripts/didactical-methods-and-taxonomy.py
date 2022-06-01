from rdflib import Graph, Literal, Namespace
import random

# create namespaces
baseNs = Namespace("http://myontology.com/")
RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
MYONT = Namespace(baseNs['myont/'])
SCHEMA = Namespace("https://schema.org/")
EDUSE = Namespace(baseNs['gebruiken/'])
TAXONOMIES = Namespace(baseNs['taxonomieen/'])
EXERCISES = Namespace(baseNs['oefeningen/'])

# create input graph
inputGraph = Graph()
inputGraph.parse('../rdf-data/educationalUses.ttl')
inputGraph.parse('../rdf-data/educationalTaxonomies.ttl')

# create output graphs
resultPhaseGraph = Graph()
resultLessonGraph = Graph()
resultExerciseGraph = Graph()

resultGraphs = [resultPhaseGraph, resultLessonGraph, resultExerciseGraph]
resultPhaseGraph.parse('../rdf-data/generated-data/generated-phases-with-excerpts.ttl')
resultLessonGraph.parse('../rdf-data/generated-data/generated-lessons.ttl')
resultExerciseGraph.parse('../rdf-data/real-data/exercises.ttl')

# avoid double entries when reruning script
resultLessonGraph.remove((None, MYONT["semanticalDensity"], None))

resultPhaseGraph.remove((None, SCHEMA['interactivityType'], None))
resultPhaseGraph.remove((None, SCHEMA['educationalUse'], None))
resultPhaseGraph.remove((None, MYONT['interactivityLevel'], None))
resultPhaseGraph.remove((None, MYONT['hasCategory'], None))

resultExerciseGraph.remove((None, MYONT['hasCategory'], None))

# bind output graphs
for g in resultGraphs:
    g.bind('rdf', RDF)
    g.bind('myont', MYONT)
    g.bind('schema', SCHEMA)
    g.bind('eduse', EDUSE)
    g.bind('edutaxonomies', TAXONOMIES)
    g.bind('exercise', EXERCISES)

phases = [s for s, _, _ in resultPhaseGraph.triples((None, RDF['type'], MYONT['LessonPhase']))]
lessons = [s for s, _, _ in resultLessonGraph.triples((None, RDF['type'], MYONT['Lesson']))]
exercises = [s for s, _, _ in resultExerciseGraph.triples((None, RDF['type'], MYONT['EducationalExercise']))]

interactivityTypes = [Literal('actief', lang="nl"), Literal('receptief', lang="nl"), Literal('gemengd', lang="nl")]
interactivityLevels = [Literal('Erg laag', lang="nl"), 
                        Literal('laag', lang="nl"), 
                        Literal('gemiddeld', lang="nl"), 
                        Literal('hoog', lang="nl"), 
                        Literal('Erg hoog', lang="nl")]

semanticalDensities = [Literal('Erg laag', lang="nl"),
                        Literal('laag', lang="nl"),
                        Literal('gemiddeld', lang="nl"),
                        Literal('hoog', lang="nl"),
                        Literal('Erg hoog', lang="nl")]

educationalUses = [s for s, _, _ in inputGraph.triples((None, SCHEMA['inDefinedTermSet'], EDUSE['set']))]
educationalTaxonomyLevels = [s for s, _, _ in inputGraph.triples((None, SCHEMA['inCodeSet'], TAXONOMIES['revisedBloom']))]

# add data for every phase
for phase in phases:
    resultPhaseGraph.add((phase, SCHEMA['interactivityType'], random.choice(interactivityTypes)))
    resultPhaseGraph.add((phase, SCHEMA['educationalUse'], random.choice(educationalUses)))
    resultPhaseGraph.add((phase, MYONT['interactivityLevel'], random.choice(interactivityLevels)))
    resultPhaseGraph.add((phase, MYONT['hasCategory'], random.choice(educationalTaxonomyLevels)))

# add data for every lesson
for lesson in lessons:
    resultLessonGraph.add((lesson, MYONT['semanticalDensity'], random.choice(semanticalDensities)))

# add data for every exercise
for exercise in exercises:
    resultExerciseGraph.add((exercise, MYONT['hasCategory'], random.choice(educationalTaxonomyLevels)))

# write data
resultPhaseGraph.serialize('../rdf-data/generated-data/generated-phases-with-excerpts.ttl', format='turtle')
resultLessonGraph.serialize('../rdf-data/generated-data/generated-lessons.ttl', format='turtle')
resultExerciseGraph.serialize('../rdf-data/real-data/exercises.ttl', format='turtle')