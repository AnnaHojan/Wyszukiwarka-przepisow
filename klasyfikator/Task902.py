import math

def featprob(bayes, feature, category):
    if category not in bayes.class_count:
        return -1e300
    if (feature, category) not in bayes.feature_count:
        return math.log(0.001/float(bayes.class_count[category]))

    liczba_wspolwystepowania = float(bayes.feature_count[(feature, category)])
    liczba_wystepownia = float(bayes.class_count[category])

    logarytm = liczba_wspolwystepowania/liczba_wystepownia

    return math.log(logarytm)
