# -*- coding: utf-8 -*-

from gensim.models.keyedvectors import KeyedVectors
import re

#read the O-NET datset and store it in tuples (O*NET-SOC Code, Title, Alternate Title)
all_tuples = []
taxonomy_tuples = open('taxonomy_tuple', 'r') 
with open('taxonomy_tuple') as lines:
	for l in lines:
		splitted_line = l.split('|')
		splitted_line[2] = splitted_line[2].replace("\n", "")
		all_tuples.append(tuple(splitted_line))
	

model = KeyedVectors.load_word2vec_format('./neuvoo_w2v_bin.bin', binary=True) #load the w2v model
roles = ['project_manager_ROLE', 'nurse_ROLE', 'researcher_ROLE', 'professor_ROLE', 'driver_ROLE', 'doctor_ROLE'] #list of roles
seniority_level = ['entry', 'junior', 'intermediate', 'senior', 'lead', 'specialist', 'experienced', 'executive', 'associate', 'staff', 'assistant', 'mid-level', 'specialist', 'principal', 'partner', 'distinguished', 'advanced', 'expert', 'apprentice', 'trainee', 'deputy', 'head']


for r in roles: #for each role get the most similar words. The most simlar words could be either roles (words that finish with '_ROLE') or non roles (words that do not finish with '_ROLE')
	try:
		top_results = []
		tmp_top_results = model.most_similar(r)
		print('Most similar to \'' + str(r) + '\': ' + str(tmp_top_results)) #get the most similar words
		
		for rr in tmp_top_results:
			#split roles composed by multiple tokens
			splitted_role = rr[0].split('_')
			
			#remove the'_ROLE' keyword
			try:
				splitted_role.remove('ROLE')
			except ValueError:
				pass
				
			#remove the seniority level
			for k in splitted_role:
				if k in seniority_level:
					splitted_role.remove(k)
			
			splitted_role = ' '.join(splitted_role)
			
			#filter out roles already in top_results
			if splitted_role not in top_results and splitted_role:
				top_results.append(splitted_role)
		
		
		print('TOP RESULT W/O SENIORITY LEVELS: ' + str(top_results))
		
		
		#remove the underscore and 'ROLE' from roles
		cleaned_role = r.split('_')
		try:
			cleaned_role.remove('ROLE')
		except ValueError:
			pass  # do nothing!

		cleaned_role = ' '.join(cleaned_role)
		find_alternate_title = False
		related_roles_taxonomy = []
		
		#search cleaned_role in alternate titles and store its id
		title_id = 0
		for t in all_tuples:
			if t[2].lower() == cleaned_role:
				title_id = t[0]
				find_alternate_title = True
				break
		
		#if cleaned_role not in alternate titles, search it in titles and store its id
		if title_id == 0:
			for t in all_tuples:
				if t[1].lower() == cleaned_role:
					title_id = t[0]
					related_roles_taxonomy.append(t[1]) #append the alternate titles id
					break
		
		#if cleaned_role is in taxonomy AND the role is in alternate title, get all its related titles
		if title_id != 0 and find_alternate_title==True:
			for t in all_tuples:
				if t[0] == title_id:
					related_roles_taxonomy.append(t[2])
					print(str(r) + ' --> ' + str(t[2])) #use t[2] for re-rank
		
		#if 'cleaned_role' is not in taxonomy			
		if not related_roles_taxonomy:
			print(str(cleaned_role) + ' NOT FOUND IN TAXONOMY')
		
		print('\n\n')
	except KeyError: #error: the model does not contain the vector for the word 'r'
		print (str(r) + ' IS NOT IN THE MODEL')



	
	
	
