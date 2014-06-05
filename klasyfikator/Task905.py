from Task904 import docprob

def classify(bayes, item):
    max_prob = None
    max_cat = None
    dict_cat_prob = dict()
    for category in bayes.class_count:
        prob = docprob(bayes, item, category)
        dict_cat_prob[category] = prob
    sort_list_cat_prob = sorted(dict_cat_prob, key=dict_cat_prob.get, reverse=True)
    return sort_list_cat_prob[:3]
