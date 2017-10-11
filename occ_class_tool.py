import import_data, classifier, os, create_counts

class Occupation_Classification_Tool(object):
    '''
    Creates an object which can classify a query using the word and bigram
    objects.

    Use the classify_query method and pass a string, list or file path and the
    object will write the results to the output.txt file.
    '''
    def __init__(self, word_count, bigram_count,group_index=0,text_index=1,specifity=1):
        if os.path.isfile(word_count) and os.path.isfile(bigram_count):
            self.classifier_object=classifier.Classifier(word_count,bigram_count)
        else:
            create_counts.create_counts(group_index,text_index,specifity,word_count,bigram_count)
            self.classifier_object=classifier.Classifier(word_count,bigram_count)
    def classify_query(self, query):
        if type(query)==str:
            if os.path.isfile(query):
                i=import_data.Importer(query,'|')
                self.classifier_object.create_output(i.imported)
            else:
                self.classifier_object.create_output([[query]])
        elif type(query)==list:
            temp_list=[[occs] for occs in query]
            self.classifier_object.create_output(temp_list)
        else:
            raise TypeError
