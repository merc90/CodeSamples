import heapq
import array
import os
import pickle
import re
import getopt
import glob
import sys
import time

class CommandLine:
    def __init__(self):
        option, argument = getopt.getopt(sys.argv[1:],'hl:s:')
        option = dict(option)
        if '-h' in option:	#If help option is asked in command line
            self.printHelp()	#Print the help

        if len(argument) > 0:
            print("*** ERROR: No argument files - only options! ***", file=sys.stderr)
            self.printHelp()

        if '-l' not in option:	#If input file is not provided
            print("\n*** ERROR: Must specify lexicon file name (opt: -l) ***", file=sys.stderr)
            self.printHelp()
        else:	#Otherwise file name is stored
            self.file_name = glob.glob(option['-l'])[0]
            
        if '-s' in option:	#if -s in command line
            if option['-s'] in ('char','word'):	#if option is either char or word
                self.option = option['-s']	#then option initialization
            else:	#Else warning
                warning = (
                        "*** ERROR: Label (opt: -s LABEL) not recognised! ***\n"
                        " -s must be one of: char/word")
                print(warning, file=sys.stderr)
                self.printHelp()
        else:
            self.option = 'char'	#Else default is character symbol setting
  
    def printHelp(self):	#Display for help
        print('***********************************')
        print("OPTIONS:")
        print('-h : Print this help message and exit')
        print('-l : Read input file')
        print('-s char: Take characters as symbols')
        print('-s word: Take words as symbols')
        print('***********************************')
        sys.exit()

class TreeLeaf:
	def __init__(self, symbol, probability, left = None, right = None):
		self.symbol = symbol #Symbol instance
		self.probability = probability #Probability instance
		self.left = left	#Left Node
		self.right = right	#Right Node

	def __lt__(self, other):
		return self.probability < other.probability 

class HuffmanCompress:
	def __init__(self):
		self.codes = {}		#Code dictionary
		self.mapping = {}	#Mapping dictionary
		self.word_regex = re.compile('[a-zA-Z]+|[^a-zA-Z]')	#Regex to get single word or single non-alphabetic characters.
		
	def make_probability_dictionary(self, text):
		probability = {}	#Create dictionary for probability
		total_symbols = len(text)	#Gets the total number of symbol
		for symbol in text:	#iterate through every symbol
			if symbol not in probability:	#If sumbol does not occur in the probability dictionary
				probability[symbol] = 1/total_symbols	#probability is initialized to 1 per total symbol
			else:
				probability[symbol] += 1/total_symbols	#otherwise probability is increased by 1 per total symbol
		return probability 	#Returns the probability dictionary

	def make_tree(self, probability):
		tree = []	#Initialize the list called tree
		
		for symbol in probability:	#iterate through every element in dictionary probability
			heapq.heappush(tree, TreeLeaf(symbol, probability[symbol]))	#Pushing all the symbol to the heap using the inplace heap sort thus get the sorted heap
		
		while(len(tree)>1):
			leaf1 = heapq.heappop(tree)	#Pop the last node
			leaf2 = heapq.heappop(tree)	#Pop the last node
			heapq.heappush(tree, TreeLeaf(None, leaf2.probability + leaf1.probability, leaf2, leaf1))	#Makes the 2 poped nodes child of thenode made from their addition,
																										#and then pushed into the heap
		
		self.make_codes_dictionary(heapq.heappop(tree), "")	#makes code dictionary using the heap

	def make_codes_dictionary(self, root, current_code):
		if not root:	#Return if not root
			return

		if root.symbol:	#If the root has symbol
			self.codes[root.symbol], self.mapping[current_code] = current_code, root.symbol 	#Put code and symbol in codes and mapping dictionary
			return

		self.make_codes_dictionary(root.left, current_code + "0")	#Append 0 to the code of left child
		self.make_codes_dictionary(root.right, current_code + "1")	#Append 1 to the code of right child

	def encode_text(self, text):
		byte = array.array('B')	#Create an array of byte

		encoded_text = ""	#Get and empty string
		for symbol in text: #Iterate through every symbol in text
			encoded_text += self.codes[symbol]	#append the string with the code corresponding to the symbol
			while (len(encoded_text)/8)>=1:
				byte.append(int(encoded_text[0:8], 2))
				encoded_text = encoded_text[8:]
		
		pad = 5 - (len(encoded_text) % 8)	#Padding is number of bits that does not make the byte subtracted from 5
		pad = 8 + pad if pad < 0 else pad  #if padding is negative, 8 is added to it, otherwise padding is padding
		
		for position in range(pad):	#Iterate through the range of padding
			encoded_text += '1'	#Append the padding
		encoded_text = encoded_text + "{0:03b}".format(pad)
		while len(encoded_text)/8:
				byte.append(int(encoded_text[0:8], 2))
				encoded_text = encoded_text[8:]

		return bytes(byte)	#Append the information of the padding which is formated into last three bits of binary equivalent

	def compress(self):
		start_time = time.time()

		infile,ext = os.path.splitext(config.file_name)	#Spliting the inputing file

		text = open(config.file_name, 'r+').read().strip()	#Opening the file, rading it, and striping it.
		text = self.word_regex.findall(text) if config.option == "word" else text #If the config is word then text is list of all words created using
													#regex
		
		self.make_tree(self.make_probability_dictionary(text)) #Making the tree called using the returned probability dictionary made using function
												#make probability dictionaty, which is called using text.
		
		pickle.dump(self.mapping, open(infile + "-symbol-model.pkl","wb"), protocol=4)	#Writing the code mapping into the pickle

		print("---Time to build the symbol model: %s seconds ---" % round(time.time() - start_time, 2))


		pickle.dump(infile, open("infile.pkl","wb"), protocol=4) #writing the input file name into pickle
				
		out = open(infile + ".bin", 'wb')
		start_time = time.time()
		out.write(self.encode_text(text)) #Opens the binary file in which binary sequence is written,
										#which is returned by the get_bytes function, which is called using returned value of get encode text,
										# which is called using the text
		print("---Time to encode the text: %s seconds ---" % round(time.time() - start_time, 2))

config = CommandLine() #Gets the instances of Command line class
HuffmanCompress().compress() #Calls the compress function of HuffmanCompress class