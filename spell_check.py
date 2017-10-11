import import_data, clean_data, enchant,sys,os
from nltk import word_tokenize
reload(sys)
sys.setdefaultencoding('utf8')

class Spell_Check(object):
    '''
    Class that tests tokens and attempts to correct those that are not valid.
    Heavily reliant of Enchant module.
    '''
    def __init__(self):
        '''
        When called the spell check object loads an enchant dictionary including
        a list of words from the SOC dataset.
        Also initialises the replacement lists which include common replacements
        '''
        self.spell_checker=enchant.DictWithPWL('en_GB','all_words.txt')
        #Creates a dictionary including all the words from the SOC. As the SOC
        #is the 'gold standard' all words included are assumed to be correct.
        #Many ocupation specific words are not in the Enchant english dictionary
        if os.path.isfile('replacements-single.txt'):
            i_s=import_data.Importer('replacements-single.txt','#')
        else:
            i_s=import_data.Importer(\
            'https://onsdigital.github.io/dp-classification-tools/standard-occupational-classification/data/replacements-single.txt','#')
        if os.path.isfile('replacements-full.txt'):
            i_f=import_data.Importer('replacements-full.txt','#')
        else:
            i_f=import_data.Importer(\
            'https://onsdigital.github.io/dp-classification-tools/standard-occupational-classification/data/replacements-full.txt','#')
        self.reps_full=self.lower_reps(i_f.imported)
        self.reps_sing=self.lower_reps(i_s.imported)
    def lower_reps(self,replacements):
        '''
        Ensures the replaced values are in lower case
        '''
        return [[word.lower() for word in line] for line in replacements]
    def replace_words(self, word, rep_list):
        '''
        If a word has a replacement in the replacement lists, update the value
        to the replacement
        '''
        for i in xrange(len(rep_list)):
            if word == rep_list[i][0]:
                return rep_list[i][1]
            #If the word is in the replacement list, replace it with the
            #corresponding replacement value
            else:
                pass
        return word
    def retokenize(self,l):
        '''
        When a replacement value has more than one token, the individual tokens
        must be recreated. This function unpacks lists within lists to create
        one list containing token values.
        '''
        l1=[]
        for element in l:
            if type(element)==str:
                l1.append(element)
            elif type(element)==list:
                for item in element:
                    l1.append(item)
            #This loop unzips lists within a list caused by retokenising
            #replaced strings.
            #l=['hello',['world','in','a'],'list'] will return:
            #l1=['hello','world','in','a','list'] in this loop
        return l1
    def spell_check(self,input_occ):
        '''
        Uses the Enchant dictionary check method to identify words which are not
        valid. Then uses the suggest method to return the most likely spelling.

        This is the most time consuming part of the classification process.
        '''
        if self.spell_checker.check(input_occ.capitalize()):
            #Capitalise method used as several words only appear in the
            #Enchant dictionary in the proper form and not lower case.
            return input_occ
        else:
            suggs=self.spell_checker.suggest(input_occ.capitalize())
            if len(suggs)!=0:
                return suggs[0].lower()
            #Enchant suggest returns a list of suggestions, ordered by the
            #most likely replacement - this may not always be the best.
            else:
                return ''
