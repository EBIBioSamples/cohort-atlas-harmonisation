# cohort-atlas-harmonisation
Harmonisation module of the Cohort Atlas project. The main aim of this project is to 
organize different datasets into comparable groups (or cohorts) based on common features or characteristics.

This module is responsible for performing operations to harmonize or reconcilate 
the datasets, in order to further create cohorts that can be analyzed as a single 
group in researches.

For launch and down of this module:
docker-compose up --build -d
docker-compose down

Internal and external ports are set in the evn.txt file in the root module directory: <br>
H_PORT=3000<br>
EXT_PORT=8081

Another product of EBI, named ZOOMA, is used in this module.
ZOOMA maps text to ontology terms based on curated mappings from selected datasources 
(more preferred), and by searching ontologies directly (less preferred).<br>
Documentation for ZOOMA is placed here: https://www.ebi.ac.uk/spot/zooma/docs. 

Example of the harmonisation module endpoint:
http://localhost:8081/match?path=/app/shared/sample_labels_to_annotate.csv <br>
The endpoint gives you information about ontology terms matched to the labels values 
from the .csv file. Example of the .csv file:<br>
LABELS<br>
Gender<br>
Birthdate<br>
Year of birth<br>
Agreement date<br>
Age at present<br>

This endpoint uses ZOOMA by this way:
http://www.ebi.ac.uk/spot/zooma/v2/api/services/annotate?propertyValue={label}
