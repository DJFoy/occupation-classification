import pickle,math,clean_data,operator,csv,import_data
from tqdm import tqdm

class Classifier(object):
    '''
    This Class will bring in the Counter objects for words and bigrams and
    attempt to return a group for a query.
    '''
    def __init__(self,word_count, bigram_count):
        '''
        Loads in the Count objects with the TF-IDF values for single words
        and bigrams.
        The Count objects must be stored as pickled files.
        '''
        self.word_count_data=pickle.load(open(word_count,'r'))
        self.bigram_count_data=pickle.load(open(bigram_count,'r'))
    def create_output(self,query_list,output_name='output.txt'):
        '''
        The function that takes a query and creates an output including the
        group.
        '''
        self.word_output={}
        self.bigram_output={}
        self.list_output=[]
        for occupation in tqdm(query_list):
            #TQDM provides a progress bar for longer query lists
            clean=self.clean_query(occupation)
            if len(clean.bigram_list)==0:
                self.word_output[occupation[0]]=\
                [self.return_group(clean.d[0][1],self.word_count_data),\
                'Unmatched']
                #If no bigrams are found match by single terms and return
                #unmatched for bigram scores. Allows us to classify queries
                #without bigrams in the same format as those with.
                #This approach avoids the list index error caused when there
                #are no bigrams.
            else:
                self.word_output[occupation[0]]=\
                [self.return_group(clean.d[0][1],self.word_count_data),\
                self.return_group(clean.bigram_list[0][1],self.bigram_count_data)]
            self.list_output.append([occupation[0],self.word_output[occupation[0]]])
            #Create the format for the output - include the input query as the
            #clean query is not as readable.
        with(open(output_name,'a')) as f:
            writer=csv.writer(f)
            writer.writerows(self.list_output)
            #Write the output to a file - appends so each new query is added to
            #the list.
    def cosine_similarity(self,q_tfidf,dict_tfidf):
        '''
        Returns the cosine similarity score for the query. This is the angle
        between the document and query vector. This is used as a measure for
        how similar a query is to each group.
        '''
        cos_score={}
        for group in [i for i in dict_tfidf if i!= 'All Data']:
            #Exclude All Data as this does not hold any value for classification
            cos_score[group]={}
            for word in q_tfidf:
                if word in dict_tfidf[group]:
                    cos_score[group][word]=dict_tfidf[group][word]*\
                    q_tfidf[word]
                    #Where a word is in the query and document vector, multiply
                    #the values for the dot product value
            cos_score[group]=sum(cos_score[group].values())
            #The cosine score is the dot product of two unit vectors
        return cos_score
    def query_tfidf(self,query,idf_list):
        '''
        Function to calculate the TF-IDF values for the query. Requires a query
        and an IDF list, which comes from the count object.
        '''
        tfidf={}
        for word in query:
            if word in idf_list:
                tfidf[word]=query.count(word)*idf_list[word]
                #Uses IDF value from Count object as these determine the
                #relevance of a term to each document
            else:
                pass
            #Only includes words that are in the Count objects as all other
            #words will add nothing to score and are not worth processing
        magnitude=math.sqrt(sum(x**2 for x in tfidf.values()))
        #Calculate the magnitude of the query in order to normalise the vector
        #Magnitude is the square root of the sum of the values squared.
        if magnitude !=0:
            for word in tfidf:
                tfidf[word]=tfidf[word]/magnitude
            #If the TF-IDF vector has no values, normalisation would cause
            #an error so we ignore these
        return tfidf
    def return_group(self,query,counter):
        '''
        Will return the most likely group based on the TF-IDF scores.
        '''
        score=self.cosine_similarity(self.query_tfidf(query,counter.count_idf),counter.count_tfidf)
        if max(score.values())==0:
            #If no group has any terms in common it will not be matched
            #This can be amended to provide a minimum score for terms however
            #TF-IDF cosine similarity scores should only be used for comparing
            #the similarity of the query with each group. It is not an objective
            #score of how well a query matches a group.
            return 'Unmatched'
        return max(score.iteritems(), key=operator.itemgetter(1))[0]
    def clean_query(self,query_list):
        '''
        Function to organise the query cleaning process
        '''
        query=clean_data.Cleaner(query_list,0,1)
        #Creates Cleaner object for the query
        query.add_dummy_group()
        query.create_tokens()
        query.spell_check()
        query.rem_stopwords()
        query.stem_words()
        query.create_bigrams()
        return query

def test():
    query_list=import_data.Importer('connect_occupations.txt','|')
    query=Classifier('word_count.pickle','bigram_count.pickle')
    query.create_output(query_list.imported,'test_v1.txt')

if __name__=='__main__':
    test()
