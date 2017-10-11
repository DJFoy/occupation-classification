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
        self.count_tf={}
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
            self.count_tf[key]=collections.Counter(self.d[key])
            #Creates a counter collection - this is much quicker than counting
            #each element using the .count() method
    def dict_idf(self, all_data="All Data"):
        '''
        Creates a dictionary containing the IDF value for each unique word in
        the set of words in the SOC database
        '''
        N=len(self.d.keys())-1
        #Counts the number of groups, subtracting the All Data dictionary
        check_set={}
        for key in [i for i in self.d if i != all_data]:
            check_set[key]=set(self.d[key])
        for word in tqdm(set(self.d[all_data])):
            #Only consider each unique word in All Data dictionary for speed
            i=0
            for key in [j for j in self.d if j != all_data]:
                if word in check_set[key]:
                    i+=1
            self.count_idf[word]=math.log(N/i)
    def dict_tfidf(self):
        '''
        For each group, calculate the TF-IDF value for each word.
        '''
        tf_idf={}
        for group in tqdm([i for i in self.count_tf if i!= 'All Data']):
            tf_idf[group]={}
            self.count_tfidf[group]={}
            for key in tqdm(self.count_tf[group]):
                if self.count_tf[group][key]:
                    #Check the term appears in the group, if not make it's score
                    # 0
                    tf_idf[group][key]=self.count_tf[group][key]*\
                    self.count_idf[key]
                    #TF-IDF is the product of the TF and IDF for each term in
                    #each group
                else:
                    tf_idf[group][key]=0
            magnitude=math.sqrt(sum(x**2 for x in tf_idf[group].values()))
            #Calculate the magnitude to normalise the TF-IDF vector for each
            #document
            for key in tf_idf[group]:
                self.count_tfidf[group][key]=tf_idf[group][key]/magnitude
