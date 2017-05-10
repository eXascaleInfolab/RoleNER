#THIS SCRIPT TAGS ROLES IN THE JOB TITLES

#HOW TO RUN THE SCRIPT: python test_ner_for_titles.py

import json, re
import nltk.tag.stanford as st
from itertools import groupby


input_file = open("./job_ads.json","r") #json file with job postings
output_file = open("./job_ads_with_tags.json","w") #output file 

for line in input_file:
	
	line = unicode(line, "utf-8")
	
	job_title = json.loads(line)['_source']['doc']['title'] #get the job title
	
	tagged_title = ''
	tagger = st.StanfordNERTagger('./ner-model_titles.ser.gz', './stanford-ner.jar') #load the tagger
	netagged_words = tagger.tag(job_title.encode('utf-8').split()) #list of all the words in the title
	
	for tag, chunk in groupby(netagged_words, lambda x:x[1]):
		word = " ".join(w for w, t in chunk) #get word from the title
		if tag == "ROLE": #if the tag of the word is 'ROLE'
			word = " <START:" + tag + ">" + word + "<END> " #tag the word
		tagged_title = tagged_title + word
	
	print('JOB_ID: ' + str(json.loads(line)['_source']['doc']['jobid']))
	print('ORIGINAL_TITLE: ' + str(job_title.encode('utf-8')))
	print('TAGGED_TITLE: ' + str(tagged_title.encode('utf-8')) + '\n')
	
	line = re.sub(job_title.encode('utf-8'), tagged_title.encode('utf-8'), line.encode('utf-8')) #replace the original title with the tagged title
	
	output_file.write(line) #write the job ad witht the tagged title to output_file

output_file.close()