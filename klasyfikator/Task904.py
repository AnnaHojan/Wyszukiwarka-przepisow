from Task903 import catprob
from Task902 import featprob

def docprob(bayes, item, cat):
    cat_prob = catprob(bayes, cat)
    feature = bayes.get_features(item)
    for feat in feature:
        feat_prob = featprob(bayes, feat, cat)
        cat_prob = feat_prob + cat_prob
    return cat_prob
