# Competency questions coursematerial and exercises

## Used prefixes

PREFIX schema: <https://schema.org/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX yearplan: <http://myontology.com/jaarplannen/>
PREFIX chapter: <http://myontology.com/hoofdstukken/>
PREFIX section: <http://myontology.com/secties/>
PREFIX bibo: <http://purl.org/ontology/bibo/>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX coursematerial: <http://myontology.com/cursusmateriaal/>
PREFIX myont: <http://myontology.com/myont/>
PREFIX phase: <http://myontology.com/lesfasen/>
PREFIX lesson: <http://myontology.com/lessen/>
PREFIX comp: <http://ilearn.ilabt.imec.be/vocab/onddoel/>
PREFIX exercisetype: <http://myontology.com/oefeningtypes/>

## Course material

### Contextual Statements

- Course materials are documents that can be physical or digital
- Course materials can be made by publishers, by teachers or organizations
- Course materials consist of chapters, that can be grouped together in sections

### Competency Questions

#### Which course material is used for yearplan:Test-year-plan?

SELECT DISTINCT ?coursematerial WHERE {
    yearplan:Test-year-plan myont:hasLearningResource ?coursematerial .
}

#### Into which chapters is coursematerial:publisher-material-kansrekenen split up?

SELECT DISTINCT ?chapter WHERE {
    ?chapter dcterms:isPartOf coursematerial:publisher-material-kansrekenen .
    ?chapter rdf:type bibo:Chapter .
    ?chapter bibo:chapter ?chapterIndex .
}
ORDER BY ?chapterIndex

#### Into which sections is coursematerial:teacher-material-stochastiek split up?

SELECT DISTINCT ?section WHERE {
    ?section dcterms:isPartOf coursematerial:teacher-material-stochastiek .
    ?section rdf:type bibo:BookSection .
    ?section bibo:section ?sectionIndex .
}
ORDER BY ?sectionIndex

#### What are the start and end page of chapter 4 of coursematerial:publisher-material-kansrekenen?

SELECT DISTINCT ?start ?end WHERE {
    ?chapter dcterms:isPartOf coursematerial:publisher-material-kansrekenen .
    ?chapter bibo:chapter 4 .
    ?chapter bibo:pageStart ?start .
    ?chapter bibo:pageEnd ?end .
}

#### How many lessons handle the third chapter of coursematerial:publisher-material-kansrekenen?

SELECT (count(distinct ?lesson) as ?count) WHERE {
    ?chapter dcterms:isPartOf coursematerial:publisher-material-kansrekenen .
    ?chapter rdf:type bibo:Chapter .
    ?chapter bibo:chapter 3 .
    ?chapter bibo:pageStart ?startChapter .
    ?chapter bibo:pageEnd ?endChapter .
    ?lessonPhase rdf:type myont:LessonPhase .
    ?lessonPhase schema:workFeatured ?excerpt .
    ?excerpt rdf:type bibo:Excerpt .
    ?excerpt dcterms:isPartOf coursematerial:publisher-material-kansrekenen.
    ?excerpt bibo:pageStart ?startExcerpt .
    ?excerpt bibo:pageEnd ?endExcerpt .
    FILTER (?startChapter < ?startExcerpt || ?startChapter = ?startExcerpt) .
    FILTER (?endChapter > ?endExcerpt || ?endChapter = ?endExcerpt) .
    ?lessonPhase schema:isPartOf ?lesson .
    ?lesson rdf:type myont:Lesson .
}

#### Which chapter is handled in lesson phase  phase:Test-year-plan-series3-lesson9-phase7?

SELECT DISTINCT ?chapter WHERE {
    phase:Test-year-plan-series3-lesson9-phase7 schema:workFeatured ?excerpt .
    ?excerpt rdf:type bibo:Excerpt .
    ?excerpt bibo:pageStart ?startExcerpt .
    ?excerpt bibo:pageEnd ?endExcerpt .
    ?excerpt dcterms:isPartOf ?coursematerial .
    ?chapter rdf:type bibo:Chapter .
    ?chapter dcterms:isPartOf ?coursematerial .
    ?chapter bibo:pageStart ?startChapter .
    ?chapter bibo:pageEnd ?endChapter .
    FILTER (?startChapter < ?startExcerpt || ?startChapter = ?startExcerpt) .
    FILTER (?endChapter > ?endExcerpt || ?endChapter = ?endExcerpt) .
}

#### Which chapter(s) are handled in lesson lesson:Test-year-plan-series3-lesson6?

SELECT DISTINCT ?chapter WHERE {
    ?phase schema:isPartOf lesson:Test-year-plan-series3-lesson6 .
    ?phase schema:workFeatured ?excerpt .
    ?excerpt rdf:type bibo:Excerpt .
    ?excerpt bibo:pageStart ?startExcerpt .
    ?excerpt bibo:pageEnd ?endExcerpt .
    ?excerpt dcterms:isPartOf ?coursematerial .
    ?chapter rdf:type bibo:Chapter .
    ?chapter dcterms:isPartOf ?coursematerial .
    ?chapter bibo:pageStart ?startChapter .
    ?chapter bibo:pageEnd ?endChapter .
    FILTER (?startChapter < ?startExcerpt || ?startChapter = ?startExcerpt) .
    FILTER (?endChapter > ?endExcerpt || ?endChapter = ?endExcerpt) .
}

## Exercises

### Contextual statements

#### Which exercises are in coursematerial:publisher-material-kansrekenen?

SELECT DISTINCT ?exercise WHERE {
    ?exercise rdf:type myont:EducationalExercise .
    ?exercise schema:isPartOf ?excerpt .
    ?excerpt dcterms:isPartOf coursematerial:publisher-material-kansrekenen .
}

#### Which exercises are in the second chapter of coursematerial:publisher-material-kansrekenen?

SELECT DISTINCT ?exercise WHERE {
    ?chapter rdf:type bibo:Chapter .
    ?chapter dcterms:isPartOf coursematerial:publisher-material-kansrekenen .
    ?chapter bibo:chapter 2 .
    ?chapter bibo:pageStart ?startChapter .
    ?chapter bibo:pageEnd ?endChapter .
    ?excerpt rdf:type bibo:Excerpt .
    ?excerpt dcterms:isPartOf coursematerial:publisher-material-kansrekenen .
    ?excerpt bibo:pageStart ?startExcerpt .
    ?excerpt bibo:pageEnd ?endExcerpt .
    FILTER (?startExcerpt > ?startChapter || ?startExcerpt = ?startChapter) .
    FILTER (?endExcerpt < ?endChapter || ?endExcerpt = ?endChapter) .
    ?exercise schema:isPartOf ?excerpt .
    ?exercise rdf:type myont:EducationalExercise .
}

#### Which easy exercises belong to the first chapter of coursematerial:publisher-material-kansrekenen?

TODO: why are new triples created?

SELECT DISTINCT ?exercise WHERE {
    ?chapter rdf:type bibo:Chapter .
    ?chapter dcterms:isPartOf coursematerial:publisher-material-kansrekenen .
    ?chapter bibo:chapter 1 .
    ?chapter bibo:pageStart ?startChapter .
    ?chapter bibo:pageEnd ?endChapter .
    ?excerpt rdf:type bibo:Excerpt .
    ?excerpt dcterms:isPartOf coursematerial:publisher-material-kansrekenen .
    ?excerpt bibo:pageStart ?startExcerpt .
    ?excerpt bibo:pageEnd ?endExcerpt .
    FILTER (?startExcerpt > ?startChapter || ?startExcerpt = ?startChapter) .
    FILTER (?endExcerpt < ?endChapter || ?endExcerpt = ?endChapter) .
    ?exercise schema:isPartOf ?excerpt .
    ?exercise rdf:type myont:EducationalExercise .
    ?exercise schema:educationalLevel "gemakkelijk"@nl .
}

#### Which exercises handle competency comp:sec-6.2-2258842063?

SELECT DISTINCT ?exercise WHERE {
    ?exercise rdf:type myont:EducationalExercise .
    ?exercise schema:teaches comp:sec-6.2-2258842063 .
}

#### What are the fill in questions in coursematerial:teacher-material-stochastiek?

SELECT DISTINCT ?exercise WHERE {
    ?exercise schema:learningResourceType exercisetype:FillInQuestion .
    ?exercise schema:isPartOf ?excerpt .
    ?excerpt dcterms:isPartOf coursematerial:teacher-material-stochastiek .
}