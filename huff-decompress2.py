import os
import pickle
import time

class HuffmanDecompress:

	def __init__(self):
		self.file_name = pickle.load(open("infile.pkl","rb")) #Gets the input file name

	def decompress(self):
		with open(self.file_name + ".bin", 'rb') as infile: #Opens the bin file
			encoded_text = ""	#Get an empty string for encoded text

			current_code = decoded_text = "" #Get an empty string for decoded text and the code

			code_mapping = pickle.load(open(self.file_name + "-symbol-model.pkl","rb")) #Gets the code mapping used to create the encoded text

			byte = infile.read(1)	#Read byte from the file
			while len(byte):	#Loop till the length of the byte is not zero
				encoded_text = bin(ord(byte))[2:].rjust(8,'0') # Appends binary equivalent of integer of Unicode code justified rightly to 8 character with 0
				byte = infile.read(1) #Read the byte from the file
				if not len(byte):
					encoded_text = encoded_text[:-3-int(encoded_text[-3:],2)]
				for bit in encoded_text: #Iterate through the encoded text till the last three bits plus the integer value of that last three bits, 
													#thus till the padding and the information of that padding
			
					current_code += bit	#Adds the bits to the code
					if current_code in code_mapping:	#If that code exist in mapping, do the statement
						decoded_text += code_mapping[current_code] #Statement1: Append the symbol corresponding to the code to the decoded text
						current_code = ""	#Statement2: Put code to empty
			open(self.file_name + "-decompressed.txt", 'w').write(decoded_text) #Opens the file and in that writing the decoded text.
			
start_time = time.time()
HuffmanDecompress().decompress() #Calls the decompress function
print("---Time to decode the compression: %s seconds ---" % round(time.time() - start_time, 2))