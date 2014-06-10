#-*- coding: utf-8 -*-
import re
import sys
import string
import glob


testlist = []
testlist.extend(glob.glob("doczyszczenia/*"))              
for doc in testlist:
	file=open(doc, 'r')
	words=[]
	for linia in file:
		linia = " ".join(linia.split())
		if linia != '':
			linia=re.sub(' minutes ',' ',linia)
			linia=re.sub(' hours ',' ',linia)
			linia=re.sub(' inch ',' ',linia)
			linia=re.sub(' bn ',' ',linia)
			linia=re.sub(' g ',' ',linia)
			linia=re.sub(' oz ',' ',linia)
			linia=re.sub(' ps ',' ',linia)
			linia=re.sub(' grams ',' ',linia)
			linia=re.sub(' gram ',' ',linia)
			linia=re.sub(' ts ',' ',linia)
			linia=re.sub(' tsp ',' ',linia)
			linia=re.sub(' pt ',' ',linia)
			linia=re.sub(' v ',' ',linia)
			linia=re.sub(' f ',' ',linia)
			linia=re.sub(' tb ',' ',linia)
			linia=re.sub(' cm ',' ',linia)
			linia=re.sub(' n ',' ',linia)
			linia=re.sub(' lb ',' ',linia)
			linia=re.sub(' mg ',' ',linia)
			linia=re.sub(' http ',' ',linia)
			linia=re.sub(' www ',' ',linia)
			linia=re.sub(' uk ',' ',linia)
			linia=re.sub(' calories ',' ',linia)
			linia=re.sub(' protein ',' ',linia)
			linia=re.sub(' carbohydrate ',' ',linia)
			linia=re.sub(' carbohydrates ',' ',linia)
			linia=re.sub(' cholesterol ',' ',linia)
			linia=re.sub(' sodium ',' ',linia)
			linia=re.sub(' mmmmm ',' ',linia)
			linia=re.sub(' kcal ',' ',linia)
			linia=re.sub('[0-9]',' ',linia)
			slowa = linia.split(' ')
			for slowo in slowa:
				slowo_bez_inter=slowo.strip(string.punctuation)
				words.append(slowo_bez_inter)
	file.close()
	file1=open(doc,'w+')
	for word in words:
		file1.write(word+' ')
	file1.close()