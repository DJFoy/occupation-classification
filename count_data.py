from __future__ import division
from tqdm import tqdm
import math,collections

class Counter(object):
    """
    Takes a dictionary of grouped tokens and returns the number of instances of
    each token within the group as a new dictionary
    """
    def __init__(self, d):
        self.d = d
        self.count_tf=None
        self.count_idf={}
        self.count_tfidf={}
    def dict_tf(self):
        """
        This function creates a new dictionary using each word in the set of
        each dictionary element in the input and a count of how many times that
        word appears in that dictionary element.
        This is the term frequency for each group.
        """
        for key in tqdm(self.d):
            if self.count_tf == None:
                self.count_tf = {key: {}}
            elif key not in self.count_tf:
                self.count_tf[key]={}
            else:
                pass
            self.count_tf[key]=collections.Counter(self.d[key])
    def dict_idf(self, all_data="All Data"):
        N=len(self.d.keys())-1
        check_set={}
        for key in [i for i in self.d if i != all_data]:
            check_set[key]=set(self.d[key])
        for word in tqdm(set(self.d[all_data])):
            i=0
            for key in [j for j in self.d if j != all_data]:
                if word in check_set[key]:
                    i+=1
            self.count_idf[word]=math.log(N/i)
    def dict_tfidf(self):
        tf_idf={}
        for group in tqdm([i for i in self.count_tf if i!= 'All Data']):
            tf_idf[group]={}
            self.count_tfidf[group]={}
            for key in tqdm(self.count_tf[group]):
                if self.count_tf[group][key]:
                    tf_idf[group][key]=self.count_tf[group][key]*\
                    self.count_idf[key]
                else:
                    tf_idf[group][key]=0
            magnitude=math.sqrt(sum(x**2 for x in tf_idf[group].values()))
            for key in tf_idf[group]:
                self.count_tfidf[group][key]=tf_idf[group][key]/magnitude
