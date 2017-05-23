from gensim.models.keyedvectors import KeyedVectors

model = KeyedVectors.load_word2vec_format('./neuvoo_w2v_bin.bin', binary=True) #load the w2v model
roles = ['project_manager_ROLE', 'nurse_ROLE', 'researcher_ROLE', 'professor_ROLE', 'driver_ROLE', 'doctor_ROLE'] #list of roles

for r in roles: #for each role get the most similar words. The most simlar words could be either roles (words that finish with '_ROLE') or non roles (words that do not finish with '_ROLE')
	try:
		print('Most similar to \'' + str(r) + '\': ' + str(model.most_similar(r)) + '\n') #get the most similar words 
	except KeyError: #error: the model does not contain the vector for the word 'r'
		print (str(r) + ' IS NOT IN THE MODEL')
		