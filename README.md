# RoleNER
Role Tagger for titles.

To execute the Python script run the following command: python test_ner_for_titles.py

The script reads the job postings from './data/job_ads.json', tag the titles (in case it finds roles) and create a new json file (./data/job_ads_with_tags.json) containing the job postings with the tags in the titles.

For example, suppose that the job title is 'looking for an assistant store manager with 5yr of experience.'. The NER will find the role 'assistant store manager' and it will tag the role. The tagged title will be as following: 'looking for an <START:ROLE>assistant store manager<END> with 5yr of experience.'.

Additional info:

-The 'model' folder contains the Stanford NER model trained with job roles to tag the roles in the titles.

-The 'data' folder contains a dataset with job postings used to test the NER ('job_ads.json' file').
