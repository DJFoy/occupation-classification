import nltk,re,string,sys
from nltk.corpus import stopwords
import spell_check as s_c
reload(sys)
sys.setdefaultencoding('utf8')
#Attempt to avoid encoding errors
stop = stopwords.words('english') + list(string.punctuation) + ["'s"]
#Creates a list of stopwords that we want to remove from the corpi
check=s_c.Spell_Check()
#Creates a spell check object outside of the Cleaner class to ensure the spell
#check class is only created once.

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
            #Issues with non-ASCII characters caused some later functions to
            #fail so ensured they were removed. Similarly, slashes and dashes
            #caused some words to be tokenised incorrectly so replaced with
            #space characters to ensure they were picked up.
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
                #Goes through each word in each occupation replacing words
                #from a common replacements file
            self.d[i][self.text_index]=check.retokenize(self.d[i][self.text_index])
            #Often a replacement will include a space character and needs to be
            #converted into two separate tokens
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
        '''
        Adds a dummy group value for query data to mirror data structure of
        SOC data.
        This makes it easier to cleanse query occupations to the same standard
        preventing duplication of code to cleanse SOC and query occupations.
        '''
        if type(self.d)==str:
            self.d=[[0,self.d]]
        elif type(self.d)==list:
            self.d=[[0,x] for x in self.d]
