#THIS SCRIPT TAGS ROLES IN THE JOB DESCRIPTIONS

#HOW TO RUN THE SCRIPT: python test_ner_for_descriptions.py

'''
HOW IT WORKS:
Suppose that the job description is 'XXX', then NER will find the role 'YYY' and it will tag the role. The tagged description will be as following: 'ZZZ'
'''

import json, re
import nltk.tag.stanford as st
from itertools import groupby


input_file = open("./data/job_ads.json","r") #json file with job postings
output_file = open("./data/job_ads_with_tags.json","w") #output file 

for line in input_file:
	
	line = unicode(line, "utf-8")
	
	try:
		job_description = json.loads(line)['_source']['doc']['html'] #get the job description
	
		tagged_description = ''
		tagger = st.StanfordNERTagger('./model/ner-model_descriptions.ser.gz', './model/stanford-ner.jar') #load the tagger
		netagged_words = tagger.tag(job_description.encode('utf-8').split()) #list of all the words in the description
		
		for tag, chunk in groupby(netagged_words, lambda x:x[1]):
			word = " ".join(w for w, t in chunk) #get word from the description
			if tag == "ROLE": #if the tag of the word is 'ROLE'
				word = " <START:" + tag + ">" + word + "<END> " #tag the word
			tagged_description = tagged_description + word
		
		print('JOB_ID: ' + str(json.loads(line)['_source']['doc']['jobid']))
		print('ORIGINAL_DESCRIPTION: ' + str(job_description.encode('utf-8')))
		print('TAGGED_DESCRIPTION: ' + str(tagged_description.encode('utf-8')) + '\n')
		
		line = re.sub(job_description.encode('utf-8'), tagged_description.encode('utf-8'), line.encode('utf-8')) #replace the original description with the tagged description
	
	except KeyError: #'html' section not found
		pass
	
	output_file.write(line) #write the job ad witht the tagged description to output_file

output_file.close()