#!/usr/bin/env python

# Name		  : LCards
# Description : Application prepare data for language cards from text
# Version	  : 0.0.1
# Author      : Lahmatiy



import argparse;
import os;
import operator;
import requests;
import json;



#---------------------------------------------------------------------------------------------------
def main():

	#-----------------------------------------------------------------------------------------------
	#Echo hello
	print "----------------------------------------------------------------------------";	
	print "LCards	ver. 0.0.1 	(translation by http://api.yandex.ru/dictionary/)";		
	print "----------------------------------------------------------------------------";



	#-----------------------------------------------------------------------------------------------
	#Create arguments parser and parse arguments
	parser = argparse.ArgumentParser();
	parser.add_argument("-i", "--input",  default = "./input",  dest = "input_dir", 
			help = "Read data from DIR", metavar = "DIR");
	parser.add_argument("-o", "--output",  default = "",  dest = "output_file", 
			help = "Save data to FILE", metavar = "FILE");
	parser.add_argument("-e", "--exceptions",  default = "",  dest = "exceptions_file", 
			help = "Exclude words from FILE", metavar = "FILE");
	parser.add_argument("-tk", "--translate_key",  default = "",  dest = "translate_key", 
			help = "Translate key");
	parser.add_argument("-tl", "--translate_lang",  default = "en-ru",  dest = "translate_lang", 
			help = "Translate language");
	parser.add_argument("-trp", "--trim_by_percent",  default = 0,  dest = "tr_p", 
			help = "Trim result list by percent PERCENT", metavar = "PERCENT");
	parser.add_argument("-trf", "--trim_by_freq",  default = 0,  dest = "tr_f", 
			help = "Trim result list by word frequency FREQ", metavar = "FREQ");
	parser.add_argument("-trn", "--trinm_by_number",  default = 0,  dest = "tr_n", 
			help = "Trim result list by items number NUMBER", metavar = "NUMBER");
	args = parser.parse_args();



	#-----------------------------------------------------------------------------------------------
	#Declare globals
	input_dir = args.input_dir;
	out_file = args.output_file;
	ext_file = args.exceptions_file;
	translate_key = args.translate_key;
	translate_lang = args.translate_lang;
	tr_p = args.tr_p;
	tr_f = args.tr_f;
	tr_n = args.tr_n; 
	#
	words_count = 0;
	words = {};
	exceptins = [];

	

	#-----------------------------------------------------------------------------------------------
	#Read exceptions
	if (ext_file != ""):
		#Print filename
		print "Exceptions file: " + ext_file;
		#Check existance
		if (os.path.isfile(ext_file) == False):			
			print "Exceptions file does not exists!\nExit.";
			exit();
		#Read file
		file = open(ext_file, 'r');			
		for line in file:
			exceptins.append( line.lower().replace('\n','') );
		file.closed
		#Print words count
		print "Excepted words: " + str(len(exceptins));



	#-----------------------------------------------------------------------------------------------
	#Read files
	#Print dir name
	print "Input dir: " + input_dir;
	#Check existance
	if (os.path.isdir(input_dir) == False):			
		print "Input directory does not exists!\nExit.";
		exit();

	#To store files count
	files_count = 0;

	#Loop for directory
	for file_name in os.listdir(input_dir):
		files_count += 1;	

		#Open and read file
		with open(input_dir+"/"+file_name, 'r') as file:
			file_data = file.read();
		file.closed
	
		#Read words
		word = "";
		#Loop ower characters
		for ch in file_data:			
			if (ch.isalpha() or ch == "'"):
				word += ch;
				continue;
			else:
				if (len(word) > 0):
					word = word.lower();
					words_count = words_count + 1;
					if word in words:
						words[word] = words[word] + 1;
					else:
						words[word] = 1;					
					word = "";
	
	#Print files count
	print "Input files: " + str(files_count);
	print "Input words: " + str(words_count);
	#Exit if no words
	if (words_count == 0):
		print "No words to process.\nExit."
		exit();



	#-----------------------------------------------------------------------------------------------
	#Remove exception words
	if ( len(exceptins) > 0 ):
		for key in words.keys():
			if (key in exceptins):
				words_count = words_count - words[key];
				del words[key];
		print "Words without excepted: " + str(words_count);
	#Exit if no words
	if (words_count == 0):
		print "No words to process.\nExit."
		exit();	



	#-----------------------------------------------------------------------------------------------
	#Sort words and reverse
	sorted_words = sorted(words.iteritems(), key=operator.itemgetter(1));
	sorted_words.reverse();



	#-----------------------------------------------------------------------------------------------
	#Count percents
	r = range(0,len(sorted_words))
	for i in r:
		item = sorted_words[i];
		per = (item[1]*100)  / float(words_count);
		item = item + (per,);
		sorted_words[i] = item;



	#-----------------------------------------------------------------------------------------------
	#Trim by percent , freq and number
	if (tr_n != 0):
		sorted_words = sorted_words[:int(tr_n)];
	#	
	if (tr_f != 0):
		r = range(0,len(sorted_words))
		for i in r:
			item = sorted_words[i];			
			if (item[1] < int(tr_f) ):
				sorted_words = sorted_words[:i];
				break;
	#
	if (tr_p != 0.0):
		r = range(0,len(sorted_words))
		for i in r:
			item = sorted_words[i];			
			if (item[2] < int(tr_p) ):
				sorted_words = sorted_words[:i];
				break;
	#Exit if no words
	if (len(sorted_words) == 0):
		print "No words to process.\nExit."
		exit();


	#-----------------------------------------------------------------------------------------------
	#Translate
	if ( translate_key != "" ):		
		r = range(0,len(sorted_words));
		url = "https://dictionary.yandex.net/api/v1/dicservice.json/lookup?key={0}&lang={1}&text={2}";		
		result = "OK";
		#Loop over words
		for i in r:
			#Get item
			item = sorted_words[i];
			#Do request
			if (result == "OK" or result == "NO_RESPONSE"):
				response = requests.get(url.format(translate_key,translate_lang,item[0]));
				#Check request status
				if ( int(response.status_code) == 200): result = "OK";
				if ( int(response.status_code) == 401): result = "INVALID_KEY"
				if ( int(response.status_code) == 402): result = "KEY_BLOCKED"
				if ( int(response.status_code) == 403): result = "DAY_LIMIT"
				if ( int(response.status_code) == 413): result = "TOO_LONG_TEXT"
				if ( int(response.status_code) == 501): result = "WRONG_TR_DIRECTION"
				if ( int(response.status_code) == 0)  : result = "NO_RESPONSE";
				item = item + (result,);
				#Parse response
				resp = json.loads(unicode(response.text));
				for de in resp["def"]:
					info = de["pos"] + ',' + de["ts"];
					for tr in de["tr"]:
						info = info + ',' + tr["text"] + ',' + tr["pos"];
					item = item + (info,);
			else:
				item = item + (result,);
			#Write to list
			sorted_words[i] = item;	



	#-----------------------------------------------------------------------------------------------
	#Save
	#Write header
	if ( out_file != ""): 
		file = open(out_file, 'w');
		file.write('word;frequency\;percent;state;translations\n');
	else: 
		print "word\tfreq\tpercent\t\tstate\ttranslations";

	#Write content
	for item in sorted_words:
		out = "";
		for text in item:
			out = out + unicode(text);
			if ( out_file != "" ): out = out + ';';
			else: out = out + '\t';
		
		if ( out_file != "" ): file.write(out.encode('utf8') + '\n');
		else: print out;
	
	#Close file
	if ( out_file != ""): file.close();

	#Exit
	print "Done.";



#---------------------------------------------------------------------------------------------------
#Entry point
if __name__ == '__main__':
	main();
