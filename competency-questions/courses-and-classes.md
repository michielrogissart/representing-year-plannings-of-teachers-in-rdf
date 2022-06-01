# Competency Questions and Contextual Statements

## Used prefixes

PREFIX class: <http://www.myontology.com/classes/>
PREFIX schema: <https://schema.org/>
PREFIX subject: <http://www.myontology.com/subjects/>
PREFIX course: <http://www.myontology.com/courses/>
PREFIX cred: <http://myontology.com/cred/>
PREFIX comp: <http://ilearn.ilabt.imec.be/vocab/onddoel/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX myont: <http://myontology.com/myont/>

## Classes

### Contextual statements
- A class teaches a lesson
- A class is given at a certain date
- A class has a start and end time

### Competency Questions

#### Which lesson is given in class:wisk-sec-gr3-doorstroom-2223-class203?

SELECT DISTINCT ?lesson WHERE {
    class:wisk-sec-gr3-doorstroom-2223-class203 schema:workPerformed ?lesson.
}

#### What is the start and end date and time of class:wisk-sec-gr3-doorstroom-2122-class102?

SELECT DISTINCT ?start ?end WHERE {
    class:wisk-sec-gr3-doorstroom-2122-class102 schema:startDate ?start .
    class:wisk-sec-gr3-doorstroom-2122-class102 schema:endDate ?end .
}

#### Which competencies are taught in class:wisk-sec-gr3-doorstroom-2122-class193?

SELECT DISTINCT ?comp WHERE {
    class:wisk-sec-gr3-doorstroom-2122-class193 schema:workPerformed ?lesson .
    ?lesson schema:teaches ?comp .
}

## Courses

### Contextual statements
- A course needs to be accomplished in order to acquire a credential
- A course teaches a subset of competencies that are recquired for the credential
- A course has no temporal or spatial information
- A course has a name and an (optional) description

### Competency questions

#### Which competencies need to be taught in course:wisk-sec-gr3-doorstroom?

SELECT DISTINCT ?comp WHERE {
    course:wisk-sec-gr3-doorstroom schema:teaches ?comp .
}

#### Which credential can be awarded when completing course:wisk-sec-gr3-doorstroom?

SELECT DISTINCT ?cred WHERE {
    course:wisk-sec-gr3-doorstroom schema:occupationalCredentialAwarded ?cred .
}

#### Which courses need to be followed to acquire cred:sec-gr3-doorstroom?

SELECT DISTINCT ?course WHERE {
    ?course schema:occupationlCredentialAwarded cred:sec-gr3-doorstroom .
}

#### Which courses teach comp:sec-6.20-1086234763?

SELECT DISTINCT ?course WHERE {
    ?course schema:teaches sec-6.20-1086234763 .
    ?course rdf:type schema:Course .
}

## Subjects

### Contextual statements
- A subject is a set of classes that are given throughout a time period (typically a school year)
- A subject has a schedule indicating when the classes occur
- A subject is an instance of a course with temporal and spatial information
- Different subjects can be an instance of the same course and are distincted by their temporal information (typically different school years)
- A subject has a name
- A class has a position within a subject
- A subject teaches at most one year plan
- All classes within a subject belong to the same year plan

### Competency Questions

#### Which classes belong to subject:wisk-sec-gr3-doorstroom-2122?

SELECT DISTINCT ?class WHERE {
    ?class schema:subEvent subject:wisk-sec-gr3-doorstroom-2122 .
}

#### What is the name of subject:wisk-sec-gr3-doorstroom-2122?

SELECT DISTINCT ?name WHERE {
    subject:wisk-sec-gr3-doorstroom-2122 schema:name ?name .
}

#### To which credential does subject:wisk-sec-gr3-doorstroom-2122 belong?

SELECT DISTINCT ?cred WHERE {
    ?course schema:hasCourseInstance subject:wisk-sec-gr3-doorstroom-2122 .
    ?course schema:occupationalCredentialAwarded ?cred .
}

#### How many classes are there in subject:wisk-sec-gr3-doorstroom-2223?

SELECT (count(DISTINCT ?class) as ?count) WHERE {
    subject:wisk-sec-gr3-doorstroom-2223 schema:subEvent ?class .
}

#### Which position does class:wisk-sec-gr3-doorstroom-2223-class109 have in subject:wisk-sec-gr3-doorstroom-2223?

SELECT (count(DSTINCT ?prevClass) as ?pos) WHERE {
    subject:wisk-sec-gr3-doorstroom-2223 schema:subEvent ?prevClass .
    ?prevClass schema:startDate ?prevDate .
    class:wisk-sec-gr3-doorstroom-2223-class109 schema:startDate ?classDate .
    FILTER (?prevDate < ?classDate) .
}

#### Which competencies are taught in subject:wisk-sec-gr3-doorstroom-2223?

SELECT DISTINCT ?comp WHERE {
    ?course schema:hasCourseInstance subject:wisk-sec-gr3-doorstroom-2223 .
    ?course schema:teaches ?comp .
}

#### On which days do classes of subject:wisk-sec-gr3-doorstroom-2223 occur?

SELECT DISTINCT ?day WHERE {
    subject:wisk-sec-gr3-doorstroom-2223 schema:eventSchedule ?schedule .
    ?schedule schema:byDay ?day .
}

#### What are the start and end times of the classes of subject:wisk-sec-gr3-doorstroom-2223 for every day?

SELECT DISTINCT ?day ?startTime ?endTime WHERE {
    subject:wisk-sec-gr3-doorstroom-2223 schema:eventSchedule ?schedule .
    ?schedule schema:byDay ?day .
    ?schedule schema:startTime ?startTime .
    ?schedule schema:endTime ?endTime . 
}
GROUP BY ?day ?startTime ?endTime
ORDER BY ?day

#### What year plan is taught in subject:wisk-sec-gr3-doorstroom-2223?

SELECT DISTINCT ?yearPlan WHERE {
    subject:wisk-sec-gr3-doorstroom-2223 schema:workPerformed ?yearPlan .
}

#### Which competencies are not yet planned for subject:wisk-sec-gr3-doorstroom-2223?

SELECT DISTINCT ?comp WHERE {
    ?course schema:hasCourseInstance subject:wisk-sec-gr3-doorstroom-2223 .
    ?course schema:teaches ?comp .
    subject:wisk-sec-gr3-doorstroom-2223 schema:subEvent ?class .
    ?class schema:workPerformed ?lesson .
    FILTER NOT EXISTS {
        ?lesson schema:teaches ?comp .
    }
}

#### Which competencies are not yet in the year plan for subject:wisk-sec-gr3-doorstroom-2223?

SELECT DISTINCT ?comp WHERE {
    ?course schema:hasCourseInstance subject:wisk-sec-gr3-doorstroom-2223 .
    ?course schema:teaches ?comp .
    subject:wisk-sec-gr3-doorstroom-2223 schema:workPerformed ?yearPlan .

    FILTER NOT EXISTS{
        ?lessonPhase schema:teaches ?comp .
        ?lessonPhase rdf:type myont:LessonPhase .
        ?lessonPhase schema:isPartOf ?lesson .
        {
            ?lesson schema:isPartOf ?yearPlan .
        } UNION {
            ?Lesson schema:isPartOf ?series .
            ?series schema:isPartOf ?yearPlan .
        }
    }
}