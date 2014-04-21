import sys, os, tf_idf

ts = tf_idf.tfScore();
print("Welcome to the TF-IDF scorer. Input HELP for a list of functions.")

while True:

	var = raw_input("Please input command here.\n");
	var = var.split();

	# Help documentation.
	if ('HELP' in var):
		print("Supported functions include:\n - ADD_DOCUMENT(inDoc)\n - ADD_DIRECTORY(inDir)\n");

	elif ('ADD_DIRECTORY' in var):
		# If the input argument is a directory, parse each file into the score object.
		if (os.path.isdir(var[1]) or os.path.isdir(os.getcwd()+'/'+var[1])):
			for filename in os.listdir(os.getcwd()):
				if filename.endswith(".txt"):
					list_of_words = [];
					with open(filename, 'r') as open_file:
						file_text = open_file.readlines();
						for line in file_text:
							words = line.split();
							list_of_words.extend(words);
					ts.addDocument(filename[:-4], list_of_words);
		else:
			print("Input directory not found.\n");

	elif ('ADD_DOCUMENT' in var):
		with open(var[1], 'r') as open_file:
			file_text = open_file.readlines();
			for line in file_text:
				words = line.split();
				list_of_words.extend(words);
			ts.addDocument(var[1][:-4], list_of_words);

	elif ('TF-IDF' in var):
		with open(var[1], 'r') as open_file:
			file_text = open_file.readlines();
			for line in file_text:
				words = line.split();
				list_of_words.extend(words);
			ts.addDocument(var[1][:-4], list_of_words);
