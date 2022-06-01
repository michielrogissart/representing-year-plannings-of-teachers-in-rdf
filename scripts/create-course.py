from rdflib import Graph, Literal, Namespace
import isodate
from datetime import datetime, timedelta

# Namespaces
baseNs = Namespace("http://myontology.com/")
RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
COURSES = Namespace(baseNs['courses/'])
SCHEMA = Namespace("https://schema.org/")
LESSON = Namespace(baseNs['lessen/'])
MYONT = Namespace(baseNs['myont/'])
YEARPLAN = Namespace(baseNs['jaarplannen/'])
CRED = Namespace(baseNs['cred/'])
SUBJECT = Namespace(baseNs['subject/'])
CLASS = Namespace(baseNs['class/'])
SCHEDULE = Namespace(baseNs['schedules/'])

# Input graphs
inputGraph = Graph()
inputGraph.parse('../rdf-data/comp.ttl')
inputGraph.parse('../rdf-data/domain.ttl')
inputGraph.parse('../rdf-data/cred.ttl')
inputGraph.parse('../rdf-data/generated-data/generated-lessons.ttl')
inputGraph.parse('../rdf-data/generated-data/generated-yearplan.ttl')
inputGraph.parse('../rdf-data/generated-data/generated-series.ttl')

# Output graphs
courseGraph = Graph()
subjectGraph = Graph()
classGraph = Graph()
scheduleGraph = Graph()
outputGraphs = [courseGraph, subjectGraph, classGraph, scheduleGraph]

def bind_graphs():
    for g in outputGraphs:
        g.bind('rdf', RDF)
        g.bind('course', COURSES)
        g.bind('schema', SCHEMA)
        g.bind('lesson', LESSON)
        g.bind('myont', MYONT)
        g.bind('yearplan', YEARPLAN)
        g.bind('cred', CRED)
        g.bind('subject', SUBJECT)
        g.bind('class', CLASS)
        g.bind('schedule', SCHEDULE)

def runQuery(graph, sparqlFile):
    query = ""
    with open(sparqlFile, 'r') as file:
        query = ' '.join(file.readlines())
    return graph.query(query)

def scheduleToDateTimes(scheduleNode):
    dateTimes = []
    # Get start and end dates
    startDateISO = scheduleGraph.value(scheduleNode, SCHEMA['startDate'], None)
    endDateISO = scheduleGraph.value(scheduleNode, SCHEMA['endDate'], None)
    if startDateISO is None or endDateISO is None:
        print(f"No startdate or endate found for {scheduleNode}")
        return None

    startDate = isodate.parse_date(startDateISO)
    endDate = isodate.parse_date(endDateISO)

    # get timedelta
    timeDeltaISO = scheduleGraph.value(scheduleNode, SCHEMA["repeatFrequency"], None)
    if timeDeltaISO is None:
        print(f"No timedelta found for {scheduleNode}")
        return None
    timeDelta = isodate.parse_duration(timeDeltaISO)

    # get start and end time
    startTimeISO = scheduleGraph.value(scheduleNode, SCHEMA['startTime'], None)
    endTimeISO = scheduleGraph.value(scheduleNode, SCHEMA['endTime'], None)
    if startTimeISO is None or endTimeISO is None:
        print(f"No start or end time found for {scheduleNode}")
        return None

    startTime = isodate.parse_time(startTimeISO)
    endTime = isodate.parse_time(endTimeISO)

    # find first date
    daySchemaNode = scheduleGraph.value(scheduleNode, SCHEMA['byDay'], None)
    if daySchemaNode is None:
        print(f"No day found for {scheduleNode}")
        return None
    itDate = startDate
    dayString = datetime.strftime(itDate, "%A")
    delta = timedelta(days=1)
    counterCheck = 0
    while SCHEMA[dayString] != daySchemaNode and counterCheck < 7:
        itDate += delta
        dayString = datetime.strftime(itDate, "%A")
        counterCheck += 1

    if counterCheck >= 7:
        print(f"Startdate couldn't be found for {scheduleNode}")
        return None

    # construct datetimes
    holidays = [h for h in scheduleGraph.triples((scheduleNode, SCHEMA['exceptDate'], None))]
    while itDate < endDate:
        if itDate not in holidays:
            startDateTime = datetime.combine(itDate, startTime)
            endDateTime = datetime.combine(itDate, endTime)
            dateTimes.append((startDateTime, endDateTime))
        itDate += timeDelta

    return dateTimes

def createClasses(name, scheduleNodes):
    classNodes = []
    dateTimes = []
    
    # compute datetimes
    for scheduleNode in scheduleNodes:
        dateTimes.extend(scheduleToDateTimes(scheduleNode))
    
    dateTimes.sort()

    # get lessons
    lessonQueryRes = runQuery(inputGraph, '../sparql/get-lessons-in-order.sparql')
    lessonArrayInOrder = sorted(lessonQueryRes, key=lambda row: (row.seriesIndex, row.lessonIndex))
    # make classes
    for classIndex, (startDateTime, endDateTime) in enumerate(dateTimes):
        id = name + str(classIndex)
        classNode = CLASS[id]
        startDateTimeISO = isodate.datetime_isoformat(startDateTime)
        endDateTimeISO = isodate.datetime_isoformat(endDateTime)
        classNodes.append(classNode)

        # add rdf data
        classGraph.add((classNode, RDF['type'], SCHEMA['CourseInstance']))
        classGraph.add((classNode, SCHEMA['startDate'], Literal(startDateTimeISO)))
        classGraph.add((classNode, SCHEMA['endDate'], Literal(endDateTimeISO)))
        # Link class with lesson if there are still lessons not planned
        if classIndex < len(lessonArrayInOrder):
            classGraph.add((classNode, SCHEMA['workPerformed'], lessonArrayInOrder[classIndex].lesson))
    return classNodes

def createSchedules(name, dayToTimesMap, startDate, endDate, holidays):
    schedules = []
    for index, (day, times) in enumerate(dayToTimesMap.items()):
        for t in times:
            scheduleNode = SCHEDULE[name + '-' + str(index)]
            scheduleGraph.add((scheduleNode, RDF['type'], SCHEMA['Schedule']))
            scheduleGraph.add((scheduleNode, SCHEMA['repeatFrequency'], Literal("P1W")))
            scheduleGraph.add((scheduleNode, SCHEMA['byDay'], day))
            scheduleGraph.add((scheduleNode, SCHEMA['startDate'], Literal(startDate)))
            scheduleGraph.add((scheduleNode, SCHEMA['endDate'], Literal(endDate)))
            startTime, endTime = t.split('-')
            scheduleGraph.add((scheduleNode, SCHEMA['startTime'], Literal(startTime)))
            scheduleGraph.add((scheduleNode, SCHEMA['endTime'], Literal(endTime)))
            for h in holidays:
                scheduleGraph.add((scheduleNode, SCHEMA["exceptDate"], Literal(h)))
            schedules.append(scheduleNode)
    return schedules

def createSubject(name, courseNode, startDate, endDate, dayToTimesMap, holidays):
    subjectNode = SUBJECT[name]
    yearplanNode = YEARPLAN['Test-year-plan']
    desc = Literal(name + "from " + startDate + " untill " + endDate)
    identifier = Literal(name + "-" + startDate + "-" + endDate)
    
    # create schedules and classes
    schedules = createSchedules('schedule-'+name, dayToTimesMap, startDate, endDate, holidays)
    classNodes = createClasses(name+"-class", schedules) 

    # add data to graphs
    courseGraph.add((courseNode, SCHEMA['hasCourseInstance'], subjectNode))
    subjectGraph.add((subjectNode, RDF['type'], SCHEMA['CourseInstance']))
    subjectGraph.add((subjectNode, SCHEMA['workPerformed'], yearplanNode))
    subjectGraph.add((subjectNode, SCHEMA['description'], desc))
    subjectGraph.add((subjectNode, SCHEMA['identifier'], identifier))
    for s in schedules:
        subjectGraph.add((subjectNode, SCHEMA['eventSchedule'], s))

    for c in classNodes:
        subjectGraph.add((subjectNode, SCHEMA['subEvent'], c))
    
    return subjectNode

def createCourse():
    courseNode = COURSES['wisk-sec-gr3-doorstroom']
    credNode = CRED['sec-gr3-doorstroom']
    compQueryRes = runQuery(inputGraph, '../sparql/get-math-comp-gr3-doorstroom.sparql')
    identifier = Literal("wisk-sec-gr3-doorstroom-1")
    name = Literal("Wiskunde 3e graad doorstroom")
    desc = Literal("Vak wiskunde voor 3e graad in doorstroom finaliteit")

    # create schedule information for subjects
    startDate1 = "2021-09-01"
    endDate1 = "2022-06-30"
    startDate2 = "2022-09-01"
    endDate2 = "2023-06-30"
    dayToTimesMap1 = {
        SCHEMA['Monday'] : ["08:25:00-09:15:00"],
        SCHEMA['Wednesday'] : ["10:20:00-11:10:00", "11:10:00-12:00:00"],
        SCHEMA['Thursday'] : ["13:10:00-14:00:00"],
        SCHEMA['Friday'] : ["14:00:00-14:50:00"]
    }
    dayToTimesMap2 = {
        SCHEMA['Monday'] : ["09:15:00-10:05:00", "14:00:00-14:50:00"],
        SCHEMA['Tuesday'] : ["09:15:00-10:05:00"],
        SCHEMA['Wednesday'] : ["10:20:00-11:10:00", "11:10:00-12:00:00"],
        SCHEMA['Thursday'] : ["08:25:00-09:15:00"],
    }
    holidays1 = ["2021-11-01", "2021-11-11", "2021-12-25" , "2022-01-01", "2022-04-18" , "2022-05-01", "2022-05-26", "2022-06-06"]
    holidays2 = ["2022-11-01", "2022-11-11", "2022-12-25" , "2023-01-01", "2023-04-10" ,"2023-05-01", "2023-05-18", "2023-05-29"]

    # create subjects
    subjectNode1 = createSubject('wisk-sec-gr3-doorstroom-2122', courseNode, startDate1, endDate1, dayToTimesMap1, holidays1)
    subjectNode2 = createSubject('wisk-sec-gr3-doorstroom-2223', courseNode, startDate2, endDate2, dayToTimesMap2, holidays2)
    # add data to graph
    courseGraph.add((courseNode, RDF['type'], SCHEMA['Course']))
    courseGraph.add((courseNode, SCHEMA['occupationalCredentialAwarded'], credNode))
    courseGraph.add((courseNode, SCHEMA['identifier'], identifier))
    courseGraph.add((courseNode, SCHEMA['name'], name))
    courseGraph.add((courseNode, SCHEMA["description"], desc))
    for row in compQueryRes:
        courseGraph.add((courseNode, SCHEMA['teaches'], row.comp))
    courseGraph.add((courseNode, SCHEMA['hasCourseInstance'], subjectNode1))
    courseGraph.add((courseNode, SCHEMA['hasCourseInstance'], subjectNode2))

bind_graphs()
createCourse()
courseGraph.serialize('../rdf-data/generated-data/generated-courses.ttl', format='turtle')
subjectGraph.serialize('../rdf-data/generated-data/generated-subjects.ttl', format='turtle')
classGraph.serialize('../rdf-data/generated-data/generated-classes.ttl', format='turtle')
scheduleGraph.serialize('../rdf-data/generated-data/generated-schedules.ttl', format='turtle')