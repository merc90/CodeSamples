import math
class Dictionary:
	def __init__(self):
		self.dict={}

	def createDic(self):
		print("Harshad")

class Retrieve:
    # Create new Retrieve object storing index and termWeighting scheme
	def __init__(self,index,termWeighting):
		self.index = index
		self.termWeighting = termWeighting
		self.d = {}
		self.doc = {}
		self.docWeight = {}
		self.createDictionary()
		self.createDocumentWeight()
		dictionary = Dictionary()
		dictionary.createDic()

    # Method to apply query to index
	def forQuery(self,query):
		self.createMapping(query)
		pa = self.computeRanking(query)[:10]
		re = []
		for q in range(len(pa)):
			re.append(pa[q][0])
		return re

	def createDocumentWeight(self):
		for docid in self.d:
			if docid not in self.docWeight:
				self.docWeight[docid] = {}
			w_tf=0
			w_tfidf=0
			for term in self.d[docid]:
				w_tf+=self.d[docid][term]*self.d[docid][term]
				w_tfidf+=(self.d[docid][term]*math.log10(len(self.d)/len(self.index[term])))*(self.d[docid][term]*math.log10(len(self.d)/len(self.index[term])))
			self.docWeight[docid]['tf']=w_tf
			self.docWeight[docid]['tfidf']=w_tfidf

	#Method to create dictionary
	def createDictionary(self):
		for term in self.index:
			for w,s in self.index[term].items():
				if w not in self.d:
					self.d[w]={}
				if term not in self.d[w]:
					self.d[w][term] = 0
				self.d[w][term] += s

	def createMapping(self, query):
		self.doc = {}
		for term in query:
			if term in self.index:
				for w in self.index[term]:
					if w not in self.doc:
						self.doc[w]=0

	def computeRanking(self,query):
		for docid in self.doc:
			for term in query:
				if term in self.index:
					if docid in self.index[term]:
						self.doc[docid] += self.calculateTermWeight(query,term,docid)
			self.doc[docid]/=self.calculateDocumentWeight(docid)
		return sorted(self.doc.items(), key=lambda kv: kv[1], reverse=True)


	def calculateTermWeight(self,query,term,docid):
		if self.termWeighting == 'binary':
			return 1
		elif self.termWeighting == 'tf':
			return self.index[term][docid]*query[term]
		else:
			return self.index[term][docid]*(math.log10(len(self.d)/len(self.index[term])))*(query[term]*math.log10(len(self.d)/len(self.index[term])))

	def calculateDocumentWeight(self,docid):
		if self.termWeighting == 'binary':
			return math.sqrt(len(self.d[docid]))
		elif self.termWeighting == 'tf':
			return math.sqrt(self.docWeight[docid]['tf'])
		else:
			return math.sqrt(self.docWeight[docid]['tfidf'])