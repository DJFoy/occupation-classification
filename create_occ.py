'''
Script to create the 4 Occupational Classification Tool objects with different levels of specificity.
'''

if __name__=='__main__':
    import pickle, occ_class_tool
    occ1=occ_class_tool.Occupation_Classification_Tool('word_count1.pickle','bigram_count1.pickle',specifity=1)
    occ2=occ_class_tool.Occupation_Classification_Tool('word_count2.pickle','bigram_count2.pickle',specifity=2)
    occ3=occ_class_tool.Occupation_Classification_Tool('word_count3.pickle','bigram_count3.pickle',specifity=3)
    occ4=occ_class_tool.Occupation_Classification_Tool('word_count4.pickle','bigram_count4.pickle',specifity=4)
    import pickle
    with(open('occ1.pickle','wb')) as f:
        pickle.dump(occ1,f)
    with(open('occ2.pickle','wb')) as f:
        pickle.dump(occ2,f)
    with(open('occ3.pickle','wb')) as f:
        pickle.dump(occ3,f)
    with(open('occ4.pickle','wb')) as f:
        pickle.dump(occ4,f)
