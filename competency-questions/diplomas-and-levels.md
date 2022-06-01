# Competency questions credentials and levels

## Used Prefixes

PREFIX schema: <https://schema.org/> 
PREFIX ondniv: <http://ilearn.ilabt.imec.be/vocab/ondniv/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX curr1: <http://ilearn.ilabt.imec.be/vocab/curr1/>

## Levels

### Contextual Statements
- educational levels can be grouped together by grade
- educational levels have age ranges typical the pupils are in

### Competency Questions

#### Which grades belong to ondniv:sec (secundair onderwijs)?

SELECT DISTINCT ?grade WHERE {
    ?grade schema:isPartOf ondniv:sec .
} 

#### Which different levels can be followed in every grade?

SELECT DISTINCT ?grade ?level WHERE {
    ?grade schema:isPartOf ondniv:sec .
    ?level schema:inDefinedTermSet ?grade .
}

ORDER BY ?grade

#### What ages do students in ondniv:sec-gr1 typically have?

SELECT ?agerange WHERE {
    ondniv:sec-gr1 schema:typicalAgeRange ?agerange .
}

#### Which levels can students of the age range 16-17 typically be in? 

SELECT DISTINCT ?level WHERE {
    ?level rdf:type schema:DefinedTerm .
  	{
    	?level schema:typicalAgeRange "16-17".
    } UNION {
    	?level schema:inDefinedTermSet ?topDomain .
    	?topDomain schema:typicalAgeRange "16-17" .
  	}
}

## Credentials

### Contextual Statements

- Credentials are linked to a certain educational level
- Competencies need to be retrieved to acquire a credential
- There are different types of credentials

### Competency Questions

#### Which can credentials can be acquired in ondniv:sec (secundair onderwijs)?

SELECT DISTINCT ?cred WHERE {
    ?level schema:inDefinedTermSet ?grade .
    ?grade schema:isPartOf ondniv:sec .
    ?cred schema:educationalLevel ?level .
}

#### Which type of credential do you acquire when finishing ondniv:sec-gr2-doorstroom?

SELECT DISTINCT ?type WHERE {
    ?cred schema:educationalLevel ondniv:sec-gr2-doorstroom .
    ?cred schema:credentialCategory ?type .
}

#### Which credentials of the type "diploma" can be acquired?

SELECT ?cred WHERE {
    ?cred schema:credentialCategory "Diploma"@nl.
}

#### Which credentials can someone of the age range "14-15" typically acquire?

SELECT DISTINCT ?cred WHERE {
    ?cred schema:typicalAgeRange "14-15" .
    ?cred rdf:type schema:EducationalOccupationalCredential .
}

#### Which competencies (sleutelcompetenties) from the domain domain:c-stem have to be met in ondniv:sec-gr3-doorstroom?

SELECT DISTINCT ?goal WHERE {
    ?cred schema:educationalLevel ondniv:sec-gr3-doorstroom .
    ?cred rdf:type schema:EducationalOccupationalCredential .
    ?cred schema:competencyRequired ?goal .
    ?goal schema:inDefinedTermSet domain:c-stem .
    
}

#### Which competencies (bouwstenen) from the domain domain:c-historisch-bewustzijn have to be met in ondniv:sec-gr1-bstroom?

SELECT DISTINCT ?goal WHERE {
    ?cred schema:educationalLevel ondniv:sec-gr1-bstroom .
    ?cred rdf:type schema:EducationalOccupationalCredential .
    ?cred schema:competencyRequired ?goal .
    ?goal schema:inDefinedTermSet ?subdomain .
    ?subdomain schema:isPartOf curr1:c-historisch-bewustzijn .
}