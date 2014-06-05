def train (bayes, item, cat):
    wordlist = bayes.get_features(item)
    if cat not in bayes.class_count:
        bayes.class_count[cat] = 0
    bayes.class_count[cat] += 1
    for word in wordlist:
        if (word,cat) not in bayes.feature_count:
            bayes.feature_count [(word, cat)] = 0
        bayes.feature_count[(word, cat)] += 1
