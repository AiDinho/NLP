import nltk
from nltk.corpus import ppattach
import sys

class DefaultClassifier(nltk.classify.ClassifierI):
    default_label = 'N'
    def classify(self, featureset):
        return self.default_label

def default_feature(item):
    return {
            'verb': item.verb,
            'prep': item.prep,
            'noun1+verb': (item.noun1, item.verb),
            'noun1+prep': (item.noun1, item.prep),
            'verb+prep': (item.verb, item.prep),
            'verb+prep+noun2': (item.verb, item.prep, item.noun2),
            'verb+prep+noun1': (item.verb, item.prep, item.noun1),
            'prep+noun2': (item.prep, item.noun2),
            #'noun1+noun2+prep': (item.noun1, item.noun2, item.prep),
            }

train_set = [ (default_feature(item), item.attachment) for item in ppattach.attachments('training') ]
# the dev_set is like the open book exam; while the test_set is like the close book exam
dev_set = [ (default_feature(item), item.attachment) for item in ppattach.attachments('devset') ]
test_set = [ (default_feature(item), item.attachment) for item in ppattach.attachments('test') ]
#classifier = DefaultClassifier()
classifier = nltk.NaiveBayesClassifier.train(train_set)


devacc = nltk.classify.accuracy(classifier, dev_set)
testacc = nltk.classify.accuracy(classifier, test_set)

print "prep:dev:%lf" % (devacc)
print "prep:test:%lf" % (testacc)
