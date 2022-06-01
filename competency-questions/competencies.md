# Competency Questions and Contextual Statements

## Used Prefixes

PREFIX comp: <http://ilearn.ilabt.imec.be/vocab/onddoel/>
PREFIX edulevel: <http://ilearn.ilabt.imec.be/vocab/ondniv/>
PREFIX domain: <http://ilearn.ilabt.imec.be/vocab/curr1/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

## Competencies

### Contextual Statements

- A competency has a code
- A competency has a description
- A competency belongs to a curriculum 
- A competency is part of a subject
- A competency belongs to a part of the subject

### Competency Questions

#### What is the description of competency sec-6.4-4053933275?

SELECT ?def WHERE {
    comp:sec-6.4-4053933275 schema:description ?def
}

#### Which basic math competencies ('bouwstenen') does a student need to acquire?

SELECT DISTINCT ?doel WHERE {
    ?doel schema:inDefinedTermSet domain:c-stem .
}

#### To which part of math does competency sec-6.4-4053933275 belong?

SELECT DISTINCT ?subdomein WHERE {
    comp:sec-6.4-4053933275 schema:inDefinedTermSet ?subdomein .
    ?subdomein schema:isPartOf domain:c-stem .
}

## Curriculum

### Contextual Statements

- A curriculum is a collection of competencies in the same domain
- A curriculum has a definition
- A curriculum can be split up into parts

### Competency Questions

#### What is the definition of curriculum c-lichamelijk-geestelijk-en-emotioneel-welzijn?
SELECT ?def WHERE {
    domain:c-lichamelijk-geestelijk-en-emotioneel-welzijn schema:description ?def.
}

#### What are the competencies required for curriculum c-andere-talen?

SELECT DISTINCT ?doel WHERE {
    ?doel schema:inDefinedTermSet domain:c-andere-talen .
}

#### In which parts is the curriculum c-stem split up?

SELECT ?subdomein WHERE {
    ?subdomein schema:isPartOf domain:c-stem .
}

