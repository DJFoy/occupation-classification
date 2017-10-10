import pickle,math,clean_data,operator,csv,import_data
from tqdm import tqdm

class Classifier(object):
    '''
    This Class will bring in the Counter objects for words and bigrams and
    attempt to return a group for a list of query terms.
    '''
    def __init__(self,word_count, bigram_count):
        self.word_count_data=pickle.load(open(word_count,'r'))
        self.bigram_count_data=pickle.load(open(bigram_count,'r'))
    def create_output(self,query_list,output_name='output.txt'):
        self.word_output={}
        self.bigram_output={}
        self.list_output=[]
        for occupation in tqdm(query_list):
            clean=self.clean_query(occupation)
            if len(clean.bigram_list)==0:
                self.word_output[occupation[0]]=\
                [self.return_group(clean.d[0][1],self.word_count_data),\
                'Unmatched']
            else:
                self.word_output[occupation[0]]=\
                [self.return_group(clean.d[0][1],self.word_count_data),\
                self.return_group(clean.bigram_list[0][1],self.bigram_count_data)]
            self.list_output.append([occupation[0],self.word_output[occupation[0]]])
        with(open(output_name,'a')) as f:
            writer=csv.writer(f)
            writer.writerows(self.list_output)
    def cosine_similarity(self,q_tfidf,dict_tfidf):
        cos_score={}
        for group in [i for i in dict_tfidf if i!= 'All Data']:
            cos_score[group]={}
            for word in q_tfidf:
                if word in dict_tfidf[group]:
                    cos_score[group][word]=dict_tfidf[group][word]*\
                    q_tfidf[word]
            cos_score[group]=sum(cos_score[group].values())
        return cos_score
    def query_tfidf(self,query,idf_list):
        tfidf={}
        for word in query:
            if word in idf_list:
                tfidf[word]=query.count(word)*idf_list[word]
            else:
                pass
        magnitude=math.sqrt(sum(x**2 for x in tfidf.values()))
        for word in tfidf:
            if magnitude !=0:
                tfidf[word]=tfidf[word]/magnitude
        return tfidf
    def return_group(self,query,counter):
        score=self.cosine_similarity(self.query_tfidf(query,counter.count_idf),counter.count_tfidf)
        if max(score.values())==0:
            return 'Unmatched'
        return max(score.iteritems(), key=operator.itemgetter(1))[0]
    def clean_query(self,query_list):
        query=clean_data.Cleaner(query_list,0,1)
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
