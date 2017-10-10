import import_data, clean_data, group_data, count_data, pickle, sys, csv, nltk
import spell_check as s_c
check=s_c.Spell_Check()
reload(sys)
sys.setdefaultencoding('utf8')

def create_counts(group_index,text_index,specifity,word_count,bigram_count):
    i=import_data.Importer('jobrecords.txt','#')
    print(u'Imported SOC data')
    c=clean_data.Cleaner(i.imported,group_index,text_index)
    c.create_tokens()
    print(u'Created SOC tokens')
    c.rem_stopwords()
    print(u'Removed stopwords')
    for i in xrange(len(c.d)):
        for j in xrange(len(c.d[i][text_index])):
            c.d[i][text_index][j] = nltk.word_tokenize(check.replace_words(\
            check.replace_words(c.d[i][text_index][j],check.reps_sing),\
            check.reps_full))
        c.d[i][text_index]=check.retokenize(c.d[i][text_index])
    print(u'Replaced words and retokenized')
    c.rem_stopwords()
    print(u'Removed stopwords')
    all_words=group_data.Grouper(c.d,group_index,specifity,text_index)
    all_words.create_dict()
    all_words.create_corpus()
    words=sorted(set(all_words.d['All Data']))
    print(u'Created all words list')
    with(open('all_words.txt','w')) as f:
        writer=csv.writer(f)
        for word in [i for i in words if i]:
            writer.writerow([word])
    print(u'Saved all words list')
    c.stem_words()
    print(u'Words stemmed')
    c.create_bigrams()
    print(u'Bigram list created')
    g=group_data.Grouper(c.d,group_index,specifity,text_index)
    bi_g=group_data.Grouper(c.bigram_list,group_index,specifity,text_index)
    g.create_dict()
    print(u'Grouped SOC data')
    g.create_corpus()
    print(u'Created SOC corpi')
    count=count_data.Counter(g.d)
    count.dict_tf()
    print(u'Counted Term Frequencies')
    count.dict_idf()
    print(u'Counted Inverse Document Frequenices')
    count.dict_tfidf()
    print(u'Counted TF-IDF values')
    bi_g.create_dict()
    print(u'Grouped bigram data')
    bi_g.create_corpus()
    print(u'Created bigram corpi')
    bi_count=count_data.Counter(bi_g.d)
    bi_count.dict_tf()
    print(u'Counted bigram Term Frequencies')
    bi_count.dict_idf()
    print(u'Counted bigram Inverse Document Frequencies')
    bi_count.dict_tfidf()
    print(u'Counted bigram TF-IDF values')
    with open(word_count,'wb') as f:
        pickle.dump(count,f)
    print(u'Pickled word counts')
    with open(bigram_count,u'wb') as f:
        pickle.dump(bi_count,f)
    print(u'Pickle bigram counts')

if __name__=='__main__':
    #create_counts(0,1,1,'word_count.pickle','bigram_count.pickle')
    create_counts(0,1,1,'word_count_test.pickle','bigram_count_test.pickle')
