import import_data, clean_data, enchant,sys
from nltk import word_tokenize
reload(sys)
sys.setdefaultencoding('utf8')

class Spell_Check(object):
    def __init__(self):
        self.spell_checker=enchant.DictWithPWL('en_GB','all_words.txt')
        i_s=import_data.Importer('replacements-single.txt','#')
        i_f=import_data.Importer('replacements-full.txt','#')
        self.reps_full=self.lower_reps(i_f.imported)
        self.reps_sing=self.lower_reps(i_s.imported)
    def lower_reps(self,replacements):
        return [[word.lower() for word in line] for line in replacements]
    def replace_words(self, word, rep_list):
        for i in xrange(len(rep_list)):
            if word == rep_list[i][0]:
                return rep_list[i][1]
            else:
                pass
        return word
    def retokenize(self,l):
        l1=[]
        for element in l:
            if type(element)==str:
                l1.append(element)
            elif type(element)==list:
                for item in element:
                    l1.append(item)
        return l1
    def spell_check(self,input_occ):
        if self.spell_checker.check(input_occ.capitalize()):
            return input_occ
        else:
            suggs=self.spell_checker.suggest(input_occ.capitalize())
            if len(suggs)!=0:
                return suggs[0].lower()
            else:
                return ''
