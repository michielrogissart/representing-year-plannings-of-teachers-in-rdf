# Competency Questions and Contextual Statements

## Used Prefixes

PREFIX schema: <https://schema.org/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX myont: <http://myontology.com/myont/>
PREFIX lesson: <http://myontology.com/lessen/>
PREFIX eduse: <http://myontology.com/gebruiken/>
PREFIX comp: <http://ilearn.ilabt.imec.be/vocab/onddoel/>
PREFIX edutaxonomies: <http://myontology.com/taxonomieen/>
PREFIX bibo: <http://purl.org/ontology/bibo/>
PREFIX coursematerial: <http://myontology.com/cursusmateriaal/>
PREFIX chapter: <http://myontology.com/hoofdstukken/>
PREFIX dcterms: <http://purl.org/dc/terms/>

## Didactical Methods

### Contextual statements

- A lesson phase can have different interactivity types: "actief" (active), "receptief" (expositive) and "gemengd" (mixed).
- The interactivity of a lesson phase can have different levels of interactivity: from "Erg laag" (very low) to "Erg hoog" (very high).
- A lesson phase can have a use, like remediating or introducing new subject matter.
- Lessons can have different semantical densities, from "Erg laag" (very low) to "Erg hoog" (very high).

### Competency questions

#### Which lesson phasese are active?

#### How many active lesson phases are there in lesson:Test-year-plan-series3-lesson11?

SELECT (count(distinct ?activePhase) as ?count)
WHERE {
    ?activePhase schema:interactivityType "actief"@nl .
    ?activePhase rdf:type myont:LessonPhase .
    ?activePhase schema:isPartOf lesson:Test-year-plan-series3-lesson11 .
    ?lesson rdf:type myont:Lesson .
}

### What are the top 5 lessons with the most expositive phases?

SELECT DISTINCT ?lesson (count(?lesson) as ?lcount) WHERE {
  ?phase schema:interactivityType "receptief"@nl.
  ?phase rdf:type myont:LessonPhase .
  ?phase  schema:isPartOf ?lesson .
  ?lesson rdf:type myont:Lesson .
}
GROUP BY ?lesson
ORDER BY DESC(?lcount)
LIMIT 5

#### Which lessons phases have a high or very high level of interactivity?

SELECT DISTINCT ?phase ?iLevel WHERE {
    ?phase myont:interactivityLevel ?iLevel .
    ?phase rdf:type myont:LessonPhase .
  	FILTER (str(?iLevel) = "hoog" || str(?iLevel) = "Erg hoog") .
}

#### Which lesson phases are used to introduce new subject matter?

SELECT DISTINCT ?phase WHERE {
    ?phase schema:educationalUse eduse:introduction .
    ?phase rdf:type myont:LessonPhase .
}

#### Which lesson phases that introduce new subject matter, have a rehearsing lesson phase before them? 

SELECT DISTINCT ?phase WHERE {
    ?phase schema:educationalUse eduse:introduction .
    ?phase rdf:type myont:LessonPhase .
    ?phase schema:isPartOf ?lesson .
    ?phase schema:position ?phasePos .
    ?prePhase schema:isPartOf ?lesson .
    ?prePhase schema:educationalUse eduse:rehearse .
    ?prePhase schema:position ?prePhasePos .
    FILTER (?prePhasePos < ?phasePos)
}

#### Which lesson phases have a high interactivity and introduce new subject matter?

SELECT DISTINCT ?phase WHERE {
    ?phase myont:interactivityLevel "hoog"@nl .
    ?phase schema:educationalUse eduse:introduction .
    ?phase rdf:type myont:LessonPhase .
}

#### Which lesson phases within a lesson of high or very high semantical density, introduce new subject matter?

SELECT DISTINCT ?lesson ?phase WHERE {
    ?lesson myont:semanticalDensity ?sd .
    ?lesson rdf:type myont:Lesson .
    FILTER (str(?sd) = "hoog" || str(?sd) = "Erg hoog").
    ?phase schema:isPartOf ?lesson .
    ?phase schema:educationalUse eduse:introduce .
    ?phase rdf:type myont:LessonPhase .
}
ORDER BY ?lesson

#### How many lessons have a low or very low semantical density?

SELECT (count(distinct ?lesson) as ?count) {
    ?lesson myont:semanticalDensity ?sd .
    ?lesson rdf:type myont:Lesson .
    FILTER (str(?sd) = "Erg laag" || str(?sd) = "laag").
}

#### Are there any phases that remediate comp:sec-6.3-505820677?

ASK {
    ?phase schema:teaches comp:sec-6.3-505820677 .
  	?phase schema:isPartOf ?lesson .
  	?phase schema:educationalUse eduse:remediation .
}

## Educational taxonomies

### Contextual statements

- An educational taxonomy is a set of categories representing on which level possess subject matter
- Exercises, as well as lesson phases can be categorised 
- The revised taxonomy of bloom consists of following levels (in order):
    1. Remember
    2. Understand
    3. Apply
    4. Analyze
    5. Evaluate
    6. Create

### Competency questions

#### What are the categories of the revised taxonomy of Bloom? What are there descriptions and in which order to they appear?

SELECT DISTINCT ?cat ?desc WHERE {
    ?cat schema:inCodeSet edutaxonomies:revisedBloom .
    ?cat schema:description ?desc .
  	FILTER (lang(?desc) = 'nl') .
    ?cat schema:codeValue ?cv .
}
ORDER BY ?cv

#### Which exercises make pupils apply comp:sec-6.11-696981899?

SELECT DISTINCT ?ex WHERE {
  ?ex schema:teaches comp:sec-6.11-696981899 .
  ?ex rdf:type myont:EducationalExercise .
  ?ex myont:hasCategory edutaxonomies:revisedBloom-apply .
}

#### Which exercises of chapter:publisher-material-kansrekenen-chapter1 reside on the evaluation level of the revised taxonomy of Bloom?

SELECT DISTINCT ?ex WHERE {
  ?ex rdf:type myont:EducationalExercise .
  ?ex myont:hasCategory edutaxonomies:revisedBloom-evaluate .
  ?ex schema:isPartOf ?excerpt .
  chapter:publisher-material-kansrekenen-chapter1 dcterms:isPartOf ?material .
  ?excerpt dcterms:isPartOf ?material .
  ?excerpt bibo:pageStart ?exStart .
  ?excerpt bibo:pageEnd ?exEnd .
  chapter:publisher-material-kansrekenen-chapter1 bibo:pageStart ?chStart .
  chapter:publisher-material-kansrekenen-chapter1 bibo:pageEnd ?chEnd.
  FILTER (?exStart > ?chStart || ?exStart = ?chStart) .
  FILTER (?exEnd < ?chEnd || ?exEnd = ?chEnd) .
}



#### On which levels of the revised taxonomy of Bloom do the lesson phases of lesson:Test-year-plan-series4-lesson7 reside?

SELECT ?cat WHERE {
  ?phase schema:isPartOf lesson:Test-year-plan-series4-lesson7.
  ?phase rdf:type myont:LessonPhase .
  ?phase myont:hasCategory ?cat .
  ?cat schema:inCodeSet edutaxonomies:revisedBloom .
}

#### On which levels of the revised taxonomy of Bloom do the exercises of lesson:Test-year-plan-series4-lesson9 reside?

SELECT ?cat WHERE {
  ?phase schema:isPartOf lesson:Test-year-plan-series4-lesson9 .
  ?phase rdf:type myont:LessonPhase .
  ?phase myont:hasLearningResource ?ex .
  ?ex rdf:type myont:EducationalExercise .
  ?ex myont:hasCategory ?cat .
  ?cat schema:inCodeSet edutaxonomies:revisedBloom .
}


