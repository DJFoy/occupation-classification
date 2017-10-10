import nltk,re,string,sys
from nltk.corpus import stopwords
import spell_check as s_c
reload(sys)
sys.setdefaultencoding('utf8')
stop = stopwords.words('english') + list(string.punctuation) + ["'s"]
check=s_c.Spell_Check()

class Cleaner(object):
    """
    A collection of functions to cleanse and create tokens for matching
    The object takes one parameter, the dataset containing the strings to be
    cleansed.
    Functions to create tokens and stem the tokens are found in this object
    """
    def __init__(self, d, group_index, text_index):
        self.d = d
        self.text_index=text_index
        self.group_index=group_index
        self.bigram_list=[]
        #Initialises the object to load the data as an attribute
    def create_tokens(self):
        """
        Use the NLTK tokenizer to create a list of tokens from each entries
        string. Returns a list of lower case words/tokens
        """
        for l in self.d:
            l[self.text_index]=nltk.word_tokenize(\
            re.sub(r'[^\x00-\x7F]+','',re.sub(r'[\/]+',' ',l[self.text_index])\
            .lower().replace('-',', ')))
    def spell_check(self):
        '''
        Use the Enchant module to check the spelling of input words, and replace
        with the most likely correct spelling.
        Also use the replacements list from ONS to correct common abbreviateions
        '''
        for i in xrange(len(self.d)):
            for j in xrange(len(self.d[i][self.text_index])):
                self.d[i][self.text_index][j]=\
                nltk.word_tokenize(check.replace_words(check.replace_words(\
                check.spell_check(self.d[i][self.text_index][j]),\
                check.reps_sing),check.reps_full))
            self.d[i][self.text_index]=check.retokenize(self.d[i][self.text_index])
    def create_bigrams(self):
        """
        This creates a bigram from the text field, that is any combination of
        two words within the string.
        We do not specify that the words must be next to each other and in
        order as the data is not in the correct order.
        """
        self.bigram_list = [[l[self.group_index],\
        [(l[self.text_index][i], l[self.text_index][j])\
        for i in xrange(len(l[self.text_index]))\
        for j in xrange(len(l[self.text_index]))\
        if l[self.text_index][j]>l[self.text_index][i]]] for l in self.d\
        if len(l[self.text_index]) > 1]
        #Two list comprehensions; the first creates a list containing the group
        #data and then another list containing all combinations of words in
        #the text field. We specifiy that one word is higher than the other to
        #remove duplicate entries reversed. The tuples are sorted alphabetically
        #so (b,a) and (a,b) will always match.
    def stem_words(self):
        """
        Uses the NLTK stemmer function to attempt to reduce variation across
        words with the same semantic value
        """
        porter=nltk.PorterStemmer()
        for l in self.d:
            l[self.text_index]=[porter.stem(w) for w in l[self.text_index]]
    def rem_stopwords(self):
        """
        Use a list of NLTK stopwords and punctuation to remove all extraneous
        tokens from the list
        """
        for l in self.d:
            l[self.text_index]=[token for token in l[self.text_index]\
            if token not in stop]
    def add_dummy_group(self):
        if type(self.d)==str:
            self.d=[[0,self.d]]
        elif type(self.d)==list:
            self.d=[[0,x] for x in self.d]
