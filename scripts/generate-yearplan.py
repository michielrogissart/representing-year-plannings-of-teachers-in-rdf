from rdflib import Graph, Literal, Namespace
from random import randint, choice

# Define namespaces
baseNs = Namespace("http://myontology.com/")
RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
SCHEMA = Namespace("https://schema.org/")
MYONT = Namespace(baseNs['myont/'])
PHASE = Namespace(baseNs['lesfasen/'])
LESSON = Namespace(baseNs['lessen/'])
SERIES = Namespace(baseNs['lesseries/'])
YEARPLAN = Namespace(baseNs['jaarplannen/'])
DOCS = Namespace(baseNs['documenten/'])

# Make graphs
compGraph = Graph()
lesFasenGraph = Graph()
lessenGraph = Graph()
lesSeriesGraph = Graph()
jaarplanGraph = Graph()
documentenGraph = Graph()

# Array holding all math-related competencies
mathComps = []
dataGraphs = [lesFasenGraph, lessenGraph, lesSeriesGraph, jaarplanGraph, documentenGraph]

# Add necessary bindings to graphs
def bind_graphs():
    for g in dataGraphs:
        g.bind("rdf", RDF)
        g.bind("schema", SCHEMA)
        g.bind("myont", MYONT)
        g.bind("phase", PHASE)
        g.bind("lesson", LESSON)
        g.bind("series", SERIES)
        g.bind("yearplan", YEARPLAN)
        g.bind("document", DOCS)

# Fill array with math-related competencies
def fill_comps():
    compGraph.parse("../rdf-data/comp.ttl")

    mathCompQuery = """
        SELECT DISTINCT ?comp WHERE {
            ?comp a schema:DefinedTerm .
            ?comp schema:identifier ?id .
            FILTER (strStarts(?id, \"sec-6\"))
        }
    """

    mathCompsTemp = compGraph.query(mathCompQuery)
    mathComps.extend([row.comp for row in mathCompsTemp])

def handlePhaseDescription(phaseName):
    path = "../rdf-data/generated-data/documents/doc-" + phaseName + ".md"
    mdText = f"""
# Description of {phaseName}
## Description
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
    """
    with open(path, "w") as f:
        f.write(mdText.strip())
    
    docNode = DOCS["doc-"+phaseName]
    documentenGraph.add((docNode, RDF['type'], SCHEMA['DigitalDocument']))
    documentenGraph.add((docNode, SCHEMA['encodingFormat'], Literal("text/markdown")))

    return docNode

def generateLessonPhase(name, position, lesNode):
    # Generate data
    durationMinutes = randint(0, 10)
    durationSeconds = randint(0, 60)
    duration = f"PT{durationMinutes}M{durationSeconds}S"
    desc = f"Lessonphase description of {name}"

    docNode = handlePhaseDescription(name)
    nrComps = randint(0,3)
    lessonPhaseComps = []
    for _ in range(nrComps):
        lessonPhaseComps.append(choice(mathComps))
    



    # Make node
    lessonPhaseNode = PHASE[name]

    # Add data to graph
    lesFasenGraph.add((lessonPhaseNode, RDF['type'], MYONT['LessonPhase']))
    lesFasenGraph.add((lessonPhaseNode, SCHEMA['name'], Literal(name)))
    lesFasenGraph.add((lessonPhaseNode, SCHEMA['description'], Literal(desc)))
    lesFasenGraph.add((lessonPhaseNode, MYONT['describedBy'], docNode))
    lesFasenGraph.add((lessonPhaseNode, SCHEMA['timeRequired'], Literal(duration)))
    lesFasenGraph.add((lessonPhaseNode, SCHEMA['position'], Literal(position)))
    lesFasenGraph.add((lessonPhaseNode, SCHEMA['isPartOf'], lesNode))

    for comp in lessonPhaseComps:
        lesFasenGraph.add((lessonPhaseNode, SCHEMA['teaches'], comp))


def generateLesson(name, position, lessonSeriesNode):
    # Make node
    lessonNode = LESSON[name]

    # Add lesson to graph
    lessenGraph.add((lessonNode, RDF['type'], MYONT['Lesson']))
    lessenGraph.add((lessonNode, SCHEMA['url'], Literal(lessonNode)))
    lessenGraph.add((lessonNode, SCHEMA['name'], Literal(name)))
    lessenGraph.add((lessonNode, SCHEMA['position'], Literal(position)))
    lessenGraph.add((lessonNode, SCHEMA['isPartOf'], lessonSeriesNode))

    # Generate and add lesson phases
    nrPhases = randint(6, 10)
    for i in range(nrPhases):
        generateLessonPhase(f"{name}-phase{i+1}", i+1, lessonNode)


def generateLessonSeries(name, position, yearPlanNode):
    # Make node
    lesSeriesNode = SERIES[name]

    # Add lesson series to graph
    lesSeriesGraph.add((lesSeriesNode, RDF['type'], MYONT['LessonSeries']))
    lesSeriesGraph.add((lesSeriesNode, SCHEMA['position'], Literal(position)))
    lesSeriesGraph.add((lesSeriesNode, SCHEMA['isPartOf'], yearPlanNode))

    # Generate and add lessons
    nrLessons = randint(5,15)
    for i in range(nrLessons):
        generateLesson(f"{name}-lesson{i+1}", i+1, lesSeriesNode)


def generateYearPlan(name):
    # Make node
    yearPlanNode = YEARPLAN[name]

    # Add year plan to graph
    jaarplanGraph.add((yearPlanNode, RDF['type'], MYONT['YearPlan']))

    # Generate lesson series
    nrLessonSeries = randint(3, 6)
    for i in range(nrLessonSeries):
        generateLessonSeries(f"{name}-series{i+1}", i+1, yearPlanNode)

# Preparation work
bind_graphs()
fill_comps()

# Generate data
generateYearPlan("Test-year-plan")

# Write data
lesFasenGraph.serialize('../rdf-data/generated-data/generated-phases.ttl', format='turtle')
lessenGraph.serialize('../rdf-data/generated-data/generated-lessons.ttl', format='turtle')
lesSeriesGraph.serialize('../rdf-data/generated-data/generated-series.ttl', format='turtle')
jaarplanGraph.serialize('../rdf-data/generated-data/generated-yearplan.ttl', format='turtle')
documentenGraph.serialize('../rdf-data/generated-data/generated-documents.ttl', format="turtle")
