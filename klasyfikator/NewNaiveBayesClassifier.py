# encoding: utf-8

"""Program do testowania naiwnego klasyfikatora bayesowskiego."""

import glob
import re
import sys

import NaiveBayes
from Task901 import train
from Task905 import classify

def getwords(docname):
    """Wyznacza zbiór cech (słów)."""
    doc = open(docname).read()
    splitter = re.compile('\\W*')
    words = [s for s in splitter.split(doc)]
    return set(words)

def category(name):
    """Zwraca liste etykiet kategorii."""
    name = name.split("/")[0] # 1 powoduje list index out of range
    idx_cat_time = name.split('-_')
    idx = idx_cat_time[0]
    cat_time = idx_cat_time[1].split('^')
    cat = cat_time[0]
    time = cat_time[1].split('.')[0]
    cat_list = cat.split("_")

    #print idx
    #print time
    #print cat_list

    return cat_list

def readFeatureCount():
    alreadyDoneFeatureCount = {};
    args = ()
    try:
        f = open("feature_count.txt", "r")
        try:
            allLines = f.readlines()
        finally:
            f.close()
    except IOError:
        pass
    else:
        for line in allLines:
            sp = line.split(";")
            args = (sp[0], sp[1])
            alreadyDoneFeatureCount[args] = int(sp[2])	
    return alreadyDoneFeatureCount;

def readClassCount():
    alreadyDoneClassCount = {};
    try:
        f = open("class_count.txt", "r")
        try:
            allLines = f.readlines()
        finally:
            f.close()
    except IOError:
        pass
    else:
        for line in allLines:
            sp = line.split(";")
            alreadyDoneClassCount[sp[0]] = int(sp[1])	
    return alreadyDoneClassCount;

def cross_eval(directory, parts, verbose=False):
    """Dokonuje sprawdzenia krzyżowego."""
    correct = 0
    total = 0

    testlist = []
    trainlist = []
        
    testlist.extend(glob.glob("recipiestest/*"))
    trainlist.extend(glob.glob("recipies/*"))
        
    classifier = NaiveBayes.NaiveBayes(getwords)
    classifier.feature_count = readFeatureCount() #wczytuje z pliku dane z wczesniejszego trenowania
    classifier.class_count = readClassCount()

    if verbose:
        print ("\tTraining classifier")
    for doc in trainlist:
        categories = category(doc)
        for cat in categories:
            train(classifier, doc, cat)
#--------------------------------------------------------------------------------------------
    try:
     #Otwiera plik istniejący lub tworzy nowy i zapisuje do niego feature_count.
        resultsFile = open("feature_count.txt", "w")
        try:
            for feat in classifier.feature_count:
                string = feat[0]+";"+feat[1]+";"+str(classifier.feature_count[(feat[0], feat[1])])+"\n"
                resultsFile.write(string)
        finally:
            resultsFile.close()
    except IOError:
        pass

    try:
        resultsFile2 = open("class_count.txt", "w") #zapisuje class_count do pliku
        try:
            for cl in classifier.class_count:
                string = cl+";"+str(classifier.class_count[cl])+"\n"
                resultsFile2.write(string)
        finally:
            resultsFile2.close()
    except IOError:
        pass
#---------------------------------------------------------------------------------------------
    if verbose:
        print ("\tClassifying")
    for doc in testlist:
        bestcats = classify(classifier, doc)
        if verbose:
            print ("\t", doc, ":", bestcats, "-"),
        cats_count = 2
        correct_count = 0
        for cat in category(doc):
            for bestcat in bestcats:
                if bestcat == cat:
                    correct_count += 1
        print (correct_count, '/', cats_count)
        correct += correct_count
        total += cats_count

    three_bests = get_three_bests(classifier)
    print three_bests
    baseline(three_bests,testlist,verbose)

    return float(correct)/float(total)

# podaj trzy najczestsze kategorie
def get_three_bests(classifier):
    #print classifier.class_count
    classes_sorted = sorted(classifier.class_count, key=classifier.class_count.get, reverse=True)
    return classes_sorted[:3]
# baseline
def baseline(three_bests,testlist,verbose):
    correct = 0
    total = 0
    for doc in testlist:
        #if verbose:
            #print "\t", doc, ":", three_bests, "-",
        cats_count = 2
        correct_count = 0
        for cat in category(doc):
            for bestcat in three_bests:
                if bestcat == cat:
                    correct_count += 1
        #print correct_count, '/', cats_count
        correct += correct_count
        total += cats_count
        
    ACCURACY = float(correct)/float(total)
    print "Base line accuracy:", ACCURACY
    

if __name__ == '__main__':
    ACCURACY = cross_eval("mailbox", 10, True)
    print ("Accuracy:", ACCURACY)
