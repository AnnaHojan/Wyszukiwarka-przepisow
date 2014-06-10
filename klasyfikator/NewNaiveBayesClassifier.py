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
    name = name.split("/")[0]
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

def cross_eval(directory, parts, verbose=False):
    """Dokonuje sprawdzenia krzyżowego."""
    correct = 0
    total = 0

    testlist = []
    trainlist = []
        
    testlist.extend(glob.glob("recipiestest/*"))              
    trainlist.extend(glob.glob("recipies/*"))
        
    classifier = NaiveBayes.NaiveBayes(getwords)

    if verbose:
        print  "\tTraining classifier"
    for doc in trainlist:
        categories = category(doc)
        for cat in categories:
            train(classifier, doc, cat)
    
    if verbose:
        print "\tClassifying"
    for doc in testlist:
        bestcats = classify(classifier, doc)
        if verbose:
            print "\t", doc, ":", bestcats, "-",
        cats_count = 2
        correct_count = 0
        for cat in category(doc):
            for bestcat in bestcats:
                if bestcat == cat:
                    correct_count += 1
        print correct_count, '/', cats_count
        correct += correct_count
        total += cats_count
    
    three_bests = get_three_bests(classifier)
    print three_bests
    baseline(three_bests,testlist,verbose)
   
    ACCURACY = float(correct)/float(total)
    print "Accuracy:", ACCURACY

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
     cross_eval("mailbox", 10, True)
    
