import math

def catprob(bayes, category):
    if category not in bayes.class_count:
        return -1e300
    liczba_kategorii = 0
    for cat in bayes.class_count:
        liczba_kategorii = liczba_kategorii + bayes.class_count[cat]
    logarytm = float(bayes.class_count[category]) / float(liczba_kategorii)
    return math.log(logarytm)
