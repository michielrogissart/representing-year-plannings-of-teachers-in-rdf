# Competency Questions and Contextual statements

## Used prefixes

PREFIX comp: <http://ilearn.ilabt.imec.be/vocab/onddoel/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX schema: <https://schema.org/>
PREFIX myont: <http://myontology.com/myont/>
PREFIX phase: <http://myontology.com/lesfasen/>
PREFIX lesson: <http://myontology.com/lessen/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX myont: <http://myontology.com/myont/>
PREFIX series: <http://myontology.com/lesseries/>

## Lesson phase

### Contextual Statements
- A lesson phase a small educational instruction that has to be described
- A lesson phase covers zero or more competencies

### Competency Questions

#### How long does phase:Test-year-plan-series3-lesson4-phase3 last?
SELECT DISTINCT ?timing WHERE {
    phase:Test-year-plan-series3-lesson4-phase3 schema:timeRequired ?timing.
}

#### Which competencies does phase:Test-year-plan-series3-lesson4-phase4 teach?
SELECT DISTINCT ?comp WHERE {
    phase:Test-year-plan-series3-lesson4-phase4 schema:teaches ?comp .
}


#### Which lesson phases teach comp:sec-6.21-863546138?

SELECT DISTINCT ?lphase WHERE {
    ?lphase schema:teaches comp:sec-6.21-863546138 .
}

## Lesson

### Contextual Statements
- A lesson consists of lesson phases
- A lesson teaches all competencies of its lesson phases
- A lesson uses al didactical methods of its lesson phases
- The duration of a lesson is the sum of the durations of its lesson phases

### Competency Questions

#### Which lesson phases belong to les1 and in which order?

#### What are the durations of the phases belonging to lesson:x?

SELECT ?phase ?dur WHERE {
    ?phase schema:isPartOf lesson:Test-year-plan-series4-lesson13 .
    ?phase rdf:type myont:LessonPhase .
    ?phase schema:timeRequired ?dur .
}

#### Which competencies does lesson:Test-year-plan-series3-lesson14 teach?
SELECT DISTINCT ?comp WHERE {
    ?lphase schema:isPartOf lesson:Test-year-plan-series3-lesson14 .
    ?lphase rdf:type myont:LessonPhase .
    ?lphase schema:teaches ?comp .
}

#### In how many lesson phases does each competency appear?

SELECT ?comp (count( distinct ?lphase) as ?freq) WHERE {
    ?lphase schema:teaches ?comp .
    ?lphase rdf:type myont:LessonPhase .
}
GROUP BY ?comp

## Lesson series

### Contextual Statements

- A lesson series is made out of different lessons
- Every lesson has a unique position in the series

### Competency Questions

#### Which lessons are there in series:Test-year-plan-series2 and in which order?

SELECT DISTINCT ?lesson WHERE {
    ?lesson schema:isPartOf series:Test-year-plan-series2 .
    ?lesson rdf:type myont:Lesson .
    ?lesson schema:position ?pos .
}
ORDER BY ?pos

#### How many lessons are in series:Test-year-plan-series5?

SELECT (count (?lesson) as ?count) WHERE {
    ?lesson schema:isPartOf series:Test-year-plan-series5 .
    ?lesson rdf:type myont:Lesson .
}

#### Which competencies are taught in series:Test-year-plan-series6?
SELECT DISTINCT ?comp WHERE {
    ?lesson schema:isPartOf series:Test-year-plan-series6 .
    ?lesson rdf:type myont:Lesson .
    ?phase schema:isPartOf ?lesson .
    ?phase rdf:type myont:LessonPhase .
    ?phase schema:teaches ?comp .
}